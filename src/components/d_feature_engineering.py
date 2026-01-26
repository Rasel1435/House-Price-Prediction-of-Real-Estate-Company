import os
import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import configure_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = configure_logger("FeatureEngineering")

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values)
    return df.drop(exclude_indices, axis='index')

def perform_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.info("==> The Feature Engineering Process has been Started...")
        df = df.copy()

        # Clean up location names by stripping extra spaces
        df['location'] = df['location'].apply(lambda x: x.strip())

        # Identify locations with <= 10 data points
        location_counts = df.groupby(
            'location')['location'].count().sort_values(ascending=False)
        locations_less_than_10 = location_counts[location_counts <= 10]

        # Replace locations with less than or equal to 10 data points with 'other'
        df['location'] = df['location'].apply(
            lambda x: 'other' if x in locations_less_than_10 else x)
        logger.info(f"Location grouping complete. Unique locations remaining: {len(df.location.unique())}")

        # Create Price per Sqft for outlier detection (if needed for next step)
        df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']

        # Remove Price Per Sqft Outliers (Statistical)
        df = remove_pps_outliers(df)
        logger.info(f"PPS Outliers removed. Shape: {df.shape}")

        # Remove BHK Outliers (Logical)
        df = remove_bhk_outliers(df)
        logger.info(f"BHK Outliers removed. Shape: {df.shape}")

        # Clean up: Price_per_sqft was only for outlier detection, we can drop it now
        df = df.drop(columns=['price_per_sqft'], errors='ignore')

        summary = (
            f"\n{'='*30}\n"
            f"FEATURE ENGINEERING REPORT\n"
            f"{'='*30}\n"
            f"Total Unique Locations after grouping: {len(df.location.unique())}\n"
            f"Final Rows for Training: {df.shape[0]}\n"
            f"Final Features: {df.columns.tolist()}\n"
            f"{'='*30}"
        )
        logger.info(summary)
        return df
    
    except Exception as e:
        logger.error("Error in Feature Engineering component")
        raise CustomException(e, sys)