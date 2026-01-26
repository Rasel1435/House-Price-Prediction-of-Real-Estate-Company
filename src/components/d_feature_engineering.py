import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import configure_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = configure_logger("FeatureEngineering")
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

        summary = (
            f"\n{'='*30}\n"
            f"FEATURE ENGINEERING REPORT\n"
            f"{'='*30}\n"
            f"Total Unique Locations after grouping: {len(df.location.unique())}\n"
            f"Final Shape after Feature Engineering: {df.shape}\n"
            f"{'='*30}"
        )
        logger.info(summary)
        return df
    
    except Exception as e:
        logger.error("Error in Feature Engineering component")
        raise CustomException(e, sys)