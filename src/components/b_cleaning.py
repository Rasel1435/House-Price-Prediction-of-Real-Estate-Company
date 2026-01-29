import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import configure_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


logger = configure_logger("DataCleaning")
def cleaning_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data by:
    - Dropping duplicates
    - Handling missing values
    - Converting data types
    - Removing outliers based on business logic
    """
    try:
        logger.info("==> Starting production data cleaning process...")

        # Drop Duplicates
        duplicate_count = df.duplicated().sum()
        df = df.drop_duplicates()

        # Handle Missing Values for critical features
        df = df.dropna(subset=['size', 'location'])

        # Impute 'bath' with median
        df['bath'] = df['bath'].fillna(df['bath'].median())

        # Create 'bhk' and drop 'size'
        df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))
        df = df.drop(['size'], axis=1)

        # Define a function to convert square footage to numerical format
        def convert_sqft_to_num(x):
            try:
                tokens = str(x).split('-')
                if len(tokens) == 2:
                    return (float(tokens[0]) + float(tokens[1])) / 2
                return float(x)
            except Exception:
                return None

        # Clean 'total_sqft'
        df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)
        
        # Drop those 46 new Nulls in total_sqft
        df = df.dropna(subset=['total_sqft'])

        # Business Logic Outlier Removal
        # Removing houses where sqft per room is less than 300
        df = df[~(df.total_sqft / df.bhk < 300)]

        # Cleaning Summary Report
        summary = (
            f"\n{'='*30}\n"
            f"DATA CLEANING REPORT\n"
            f"{'='*30}\n"
            f"Rows after cleaning: {df.shape[0]} | Columns: {df.shape[1]}\n"
            f"Duplicates Removed: {duplicate_count}\n"
            f"Remaining Nulls: {df.isnull().sum()}\n"
            f"Columns Present: {df.columns.tolist()}\n"
            f"{'='*30}"
        )
        logger.info(summary)
        
        logger.info(f"==> Data cleaning process completed successfully.\n\n")
        return df

    except Exception as e:
        logger.error("Error occurred in Data Cleaning component")
        raise CustomException(e, sys)