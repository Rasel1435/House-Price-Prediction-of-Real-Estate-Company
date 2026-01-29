import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import configure_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = configure_logger("FeatureSelection")
def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Selects necessary columns and drops redundant ones based on 
    correlation analysis and missing value checks.
    """
    try:
        logger.info("Starting Feature Selection process...")

        # Define columns to keep based on notebook verification
        # This removes area_type, availability, society, and balcony
        necessary_columns = ['location', 'total_sqft', 'bath', 'price', 'bhk']
        
        # Filter the dataframe
        # This automatically resolves the 5,000+ nulls in 'society' and 'balcony'
        df_selected = df[necessary_columns].copy()

        # Logging the change
        dropped_cols = [col for col in df.columns if col not in necessary_columns]
        
        summary = (
            f"\n{'='*30}\n"
            f"FEATURE SELECTION REPORT\n"
            f"{'='*30}\n"
            f"Columns Kept: {list(df_selected.columns)}\n"
            f"Columns Dropped: {dropped_cols}\n"
            f"Final Shape: {df_selected.shape}\n"
            f"{'='*30}"
        )
        logger.info(summary)

        return df_selected

    except Exception as e:
        logger.error("Error occurred in Feature Selection component")
        raise CustomException(e, sys)