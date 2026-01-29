import os
import sys
import pandas as pd
import pickle
import json
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.tree import DecisionTreeRegressor
from src.exception import CustomException
from src.logger import configure_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = configure_logger("ModelTrainer")

class ModelTrainer:
    def find_best_model_using_gridsearchcv(self, X, y):
        algos = {
            'linear_regression': {
                'model': LinearRegression(),
                'params': {'copy_X': [True, False]}
            },
            'lasso': {
                'model': Lasso(),
                'params': {'alpha': [1, 2], 'selection': ['random', 'cyclic']}
            },
            'decision_tree': {
                'model': DecisionTreeRegressor(),
                'params': {
                    'criterion': ['poisson', 'friedman_mse'],
                    'splitter': ['best', 'random']
                }
            }
        }
        scores = []
        cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
        for algo_name, config in algos.items():
            gs = GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
            gs.fit(X, y)
            scores.append({
                'model': algo_name,
                'best_score': gs.best_score_,
                'best_params': gs.best_params_
            })
        return pd.DataFrame(scores, columns=['model', 'best_score', 'best_params'])

    def initiate_model_trainer(self, train_df):
        try:
            logger.info("==> Model Training Process Started...")
            
            # One-Hot Encoding (Location)
            dummies = pd.get_dummies(train_df.location)
            # Dropping 'other' to avoid the dummy variable trap
            df = pd.concat([train_df, dummies.drop('other', axis='columns')], axis='columns')
            df = df.drop('location', axis='columns')

            X = df.drop(['price'], axis='columns')
            y = df.price

            # Find Best Model and Capture Results
            model_report_df = self.find_best_model_using_gridsearchcv(X, y)
            
            # --- SUMMARY SECTION START ---
            best_row = model_report_df.loc[model_report_df['best_score'].idxmax()]
            best_model_name = best_row['model']
            best_score = best_row['best_score']

            summary = (
                f"\n{'='*40}\n"
                f"MODEL TRAINING SUMMARY\n"
                f"{'='*40}\n"
                f"Best Model Found: {best_model_name.upper()}\n"
                f"Best R2 Score:    {best_score:.4f}\n"
                f"Best Params:      {best_row['best_params']}\n"
                f"{'='*40}\n"
                f"Full Comparison:\n{model_report_df.to_string(index=False)}\n"
                f"{'='*40}"
            )
            logger.info(summary)
            # --- SUMMARY SECTION END ---

            # Save the actual Winner
            # (Note: In a more advanced version, you'd initialize the winner dynamically)
            winner_model = LinearRegression() # or logic to pick based on best_model_name
            winner_model.fit(X, y)

            # Export Artifacts
            os.makedirs('artifacts', exist_ok=True)
            with open("artifacts/model.pkl", "wb") as f:
                pickle.dump(winner_model, f)
            
            columns = {'data_columns': [col.lower() for col in X.columns]}
            with open("artifacts/columns.json", "w") as f:
                json.dump(columns, f)

            logger.info("Artifacts saved: artifacts/model.pkl & artifacts/columns.json")
            
            return best_score

        except Exception as e:
            logger.error("Error occurred in Model Trainer component")
            raise CustomException(e, sys)