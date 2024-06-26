import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zenml import step
from typing import Union
from config import PROCESSED_DATA_PATH, DATA_SOURCE
from error_logs import configure_logger
# Configure logger
logger = configure_logger()

@step(name="Feature Engineering", enable_step_logs=True, enable_artifact_metadata=True)
def FeatureEngineering(df: pd.DataFrame) -> Union[pd.DataFrame, None]:
    try:
        logger.info("==> The Feature Engineering Process has been Started...")
        # Create a new feature to detect outliers
        df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']

        # Clean up location names by stripping extra spaces
        df['location'] = df['location'].apply(lambda x: x.strip())

        # Group locations by count and filter out those with less than or equal to 10 data points
        location_counts = df.groupby(
            'location')['location'].count().sort_values(ascending=False)
        locations_less_than_10 = location_counts[location_counts <= 10]

        # Replace locations with less than or equal to 10 data points with 'other'
        df['location'] = df['location'].apply(
            lambda x: 'other' if x in locations_less_than_10 else x)

        logger.info("==> The Feature Engineering Process has been done SuccessFully...!")
        return df
    except Exception as e:
        logger.error(f"==> Error: {e}")
        return None


# if __name__ == "__main__":
#     df = pd.read_csv(r'C:/Users/SRA/Desktop/Real-Estate-Price-Prediction-Project/data/Final_Pipelines_Data.csv')
#     df = FeatureEngineering(df)
#     df.to_csv(PROCESSED_DATA_PATH, index=False)