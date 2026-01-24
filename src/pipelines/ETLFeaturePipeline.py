import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_SOURCE
from components.a_load import ingest_data
from components.b_cleaning import cleaning_data
from src.logger import configure_logger
from src.exception import CustomException
# Configure logger
logger = configure_logger()

def run_pipeline():
    try:
        logger.info("==> Pipeline process has been started...")
        df = ingest_data(DATA_SOURCE)
        df = cleaning_data(df)
        
        logger.info("==> Pipeline process has been done successfully!")
        return df
    except Exception as e:
        logger.error(f"==> Pipeline process has been failed: {e}")
        return None
         

if __name__ == "__main__":
    run_pipeline()


# Run: python -m src.pipelines.ETLFeaturePipeline.py

