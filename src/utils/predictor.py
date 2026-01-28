import os
import sys
import json
import pickle
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import configure_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = configure_logger("Predictor")

class HousePricePredictor:
    def __init__(self):
        self.model = None
        self.columns = None
        self.model_path = os.path.join("artifacts", "model.pkl")
        self.columns_path = os.path.join("artifacts", "columns.json")
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads the saved model and column metadata."""
        try:
            logger.info("Loading artifacts for prediction...")
            
            if not os.path.exists(self.model_path) or not os.path.exists(self.columns_path):
                raise FileNotFoundError("Model artifacts not found. Please run the ETL pipeline first.")

            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f) # Note: use pickle.load(f)
            
            with open(self.columns_path, "r") as f:
                self.columns = json.load(f)['data_columns']
                
            logger.info("Artifacts loaded successfully.")
        except Exception as e:
            raise CustomException(e, sys)

    def predict_price(self, location, sqft, bath, bhk):
        try:
            loc_index = -1
            if location.lower() in self.columns:
                loc_index = self.columns.index(location.lower())

            x = np.zeros(len(self.columns))
            x[0] = sqft
            x[1] = bath
            x[2] = bhk
            if loc_index >= 0:
                x[loc_index] = 1

            # Convert to DataFrame to match the feature names used during training
            # This removes the UserWarning
            x_df = pd.DataFrame([x], columns=self.columns)
            
            prediction = self.model.predict(x_df)[0]
            return round(prediction, 2)

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise CustomException(e, sys)

# Example usage for testing
if __name__ == "__main__":
    predictor = HousePricePredictor()
    # Test with a known location from your dataset
    price = predictor.predict_price('1st Phase JP Nagar', 1000, 2, 2)
    print(f"Estimated Price: {price} Lakhs")



# Run: python -m src.utils.predictor