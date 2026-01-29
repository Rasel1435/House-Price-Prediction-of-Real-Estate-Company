import os
import sys
import pandas as pd
from pathlib import Path
from config import DATA_SOURCE
from src.logger import configure_logger
from src.exception import CustomException

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = configure_logger("DataIngestion")



def ingest_data(DATA_SOURCE: str) -> pd.DataFrame:
    """
    This function ingests the data from the given path and returns a pandas DataFrame.
    
    Args:
    DATA_SOURCE (str): The file path to the CSV data file.
    
    Returns:
    pd.DataFrame: The ingested data as a pandas DataFrame.
    """
    try:
        logger.info("==> Starting data ingestion process...")
        # Convert string path to Path object for robust checking
        data_path = Path(DATA_SOURCE)

        # Check if the file exists
        if not data_path.exists():
            logger.error(f"Data file not found at: {data_path}")
            raise FileNotFoundError(f"Missing input data: {data_path}")
        logger.info(f"==> Ingesting data from: {data_path}")

        # Loading Process
        df = pd.read_csv(data_path)

        # Ingestion Summary
        summary = (
            f"\n{'='*30}\n"
            f"DATA INGESTION REPORT\n"
            f"{'='*30}\n"
            f"Source: {data_path.name}\n"
            f"Rows: {df.shape[0]} | Columns: {df.shape[1]}\n"
            f"File Integrity: {'PASS' if not df.empty else 'FAIL'}\n"
            f"Columns Found: {df.columns.tolist()[:5]}... (Total {len(df.columns)})\n"
            f"{'='*30}"
        )
        logger.info(summary)
        logger.info("==> Data ingestion process completed successfully.\n\n")
        return df
    

    except Exception as e:
        logger.error(f"Unexpected error during ingestion: {e}")
        raise CustomException(e, sys)
    


# ------------------------------------------
# For local testing of the ingestion step
# ------------------------------------------
"""
if __name__ == "__main__":
    df = ingest_data(DATA_SOURCE=DATA_SOURCE)
    print("Ingestion completed.")
    print(df.head())
    print(f"Data shape: {df.shape}" if df is not None else "Ingestion failed.")

"""
# Run: python -m src.components.a_load