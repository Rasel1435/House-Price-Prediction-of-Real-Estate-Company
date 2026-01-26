import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_SOURCE
from components.a_load import ingest_data
from components.b_cleaning import cleaning_data
from components.c_feature_selection import select_features
from components.d_feature_engineering import perform_feature_engineering
from src.logger import configure_logger
from src.exception import CustomException
# Configure logger
logger = configure_logger()

def run_pipeline():
    try:
        logger.info("==> Pipeline process has been started...")
        loading_df = ingest_data(DATA_SOURCE)
        cleaning_df = cleaning_data(loading_df)
        feature_selection_df = select_features(cleaning_df)
        feature_engineering_df = perform_feature_engineering(feature_selection_df)

        logger.info("==> Pipeline process has been done successfully!")
        return feature_engineering_df
    except Exception as e:
        logger.error(f"==> Pipeline process has been failed: {e}")
        return None
         

if __name__ == "__main__":
    run_pipeline()


# Run: python -m src.pipelines.ETLFeaturePipeline

