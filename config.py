import os
# DATA_SOURCE = 'online'
# In AWS, we might point this to an S3 bucket path later
DATA_SOURCE = os.getenv('DATA_SOURCE', './data/Bengaluru_House_Data.csv')
PROCESSED_DATA_PATH = os.getenv('PROCESSED_DATA_PATH', './data/Final_Pipelines_Data.csv')
# Feature Store / Metadata
FEATURE_GROUP_NAME = 'house_price_prediction'
FEATURE_GROUP_DESCRIPTION = "Real Estate House Price Prediction"
FEATURE_DESCRIPTIONS = [
    {"name": "Location", "description": "Total Location will be here it's str type"},
    {"name": "total_sqft", "description": "Total squree feet will be here"},
    {"name": "bhk", "description": "Type of Room"},
    {"name": "bath", "description": "Total bathrooms"},
    {"name": "price", "description": "Price will be here"},
]

TABLE_NAME = 'house-price-prediction'
# AWS Credentials - Pulled from Environment Variables (Safe approach)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

MODEL_NAME = 'house-price-prediction'
DOCKER = 'sha256:4bb138a44433e72016fe7913e51bd7e87ce1e27eded7fd6f1cabda24811af3f6'


# This should be our AWS ECR Repository URI, not a local Docker ID
# Example: 123456789012.dkr.ecr.us-east-1.amazonaws.com/house-price-prediction:latest
ECR_REPOSITORY_URI = os.getenv('ECR_REPOSITORY_URI', '')