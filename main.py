import sys
import os
from src.pipelines.ETLFeaturePipeline import run_pipeline
from src.utils.predictor import HousePricePredictor

def main():
    while True:
        print("\n" + "="*35)
        print(" 🏠 BENGALURU HOUSE PRICE SYSTEM 🏠 ")
        print("="*35)
        print("1. Train Model (Run Full ETL Pipeline)")
        print("2. Make a Prediction (Live Input)")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ")

        if choice == '1':
            print("\n Starting Training Pipeline...")
            try:
                # This runs your Ingestion -> Cleaning -> Training -> Artifact saving
                df_result = run_pipeline()
                if df_result is not None:
                    print("\n Model Trained and Artifacts Saved Successfully!")
                else:
                    print("\n Pipeline failed. Please check the logs for details.")
                    
            except Exception as e:
                print(f"Error during training: {e}")
                
        elif choice == '2':
            # Check if artifacts exist before predicting
            if not os.path.exists("artifacts/model.pkl"):
                print("Error: Model not found. Please run Option 1 first!")
                continue

            try:
                predictor = HousePricePredictor()
                print("\n--- Property Details ---")
                loc = input("Location (e.g. 1st Phase JP Nagar): ")
                sqft = float(input("Total Square Feet: "))
                bath = int(input("Number of Bathrooms: "))
                bhk = int(input("BHK: "))

                price = predictor.predict_price(loc, sqft, bath, bhk)
                print(f"\n Estimated Price: {price} Lakhs")
            except ValueError:
                print("Invalid input. Please enter numbers for sqft, bath, and bhk.")
            except Exception as e:
                print(f"Error: {e}. (Did you train the model first?)")

            
        elif choice == '3':
            print("Goodbye! Happy House Hunting.")
            sys.exit()
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()



# Run: python -m main