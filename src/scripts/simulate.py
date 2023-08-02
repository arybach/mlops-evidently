import sys
import os

# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

import logging
from pathlib import Path
from typing import List, Text

import pandas as pd
import random
import requests
from sqlalchemy import create_engine

from config.config import DATABASE_URI, DATA_COLUMNS
from src.utils.models import LinearRegressionPredictionTable, XGBoostPredictionTable
from src.utils.db_utils import open_sqa_session


logging.basicConfig(
    level=logging.INFO,
    format='SIMULATE - %(levelname)s - %(message)s'
)


def simulate(model_name) -> None:
    """Runs a simulation for predicting nutrients-based score of food items from usda db.
    """

    # Minimal and maximum size of the next batch
    BATCH_MIN_SIZE: int = 100
    BATCH_MAX_SIZE: int = 1000
    # Path to test data
    DATA_FEATURES_DIR: Path = Path('data/features')
    TEST_DATA_PATH: Path = DATA_FEATURES_DIR / 'testing_data.parquet'

    # Load data
    additional_columns: List[Text] = ['fid','score']
    num_features: List[Text] = DATA_COLUMNS['num_features']
    cat_features: List[Text] = DATA_COLUMNS['cat_features']
    required_columns: List[Text] = (
        additional_columns + num_features + cat_features
    )

    test_data: pd.DataFrame = pd.read_parquet(TEST_DATA_PATH)
    print(test_data.columns)  # Add this line to check the column names
    test_data = test_data.loc[:, required_columns]

    # Delete results of previous simulation
    fids: List[Text] = test_data['fid'].to_list()
    engine = create_engine(DATABASE_URI)
    session = open_sqa_session(engine)

    if model_name == 'xgboost_model':
        delete_query = (
            XGBoostPredictionTable.__table__.delete()
                                    .where(XGBoostPredictionTable.fid.in_(fids))
        )
    elif model_name == 'linear_regression_model':
        delete_query = (
            LinearRegressionPredictionTable.__table__.delete()
                                    .where(LinearRegressionPredictionTable.fid.in_(fids))
        )

    session.execute(delete_query)
    session.commit()
    session.close()

    total_rows_taken: int = 0
    total_rows = test_data.shape[0]

    # Get batches until all rows taken
    while total_rows_taken < total_rows:
        # Calculate the end row index for the current batch
        end_row: int = min(total_rows_taken + random.randint(BATCH_MIN_SIZE, BATCH_MAX_SIZE), total_rows)

        # Get batch
        batch: pd.DataFrame = test_data.iloc[total_rows_taken:end_row, :]
        # logging.info(f'Batch smaple = {batch.head()}')
        logging.info(f'Batch size = {batch.shape[0]}')

        """
        Make prediction request.
        Send data batch serialized to JSON string.
        """
        resp: requests.Response = requests.post(
            url=f'http://0.0.0.0:5000/predict/{model_name}',
            json={'features': batch.to_json()}
        )

        if resp.status_code == 200:
            # If OK then extract predictions
            if resp.json().get('predictions'):
                preds_json: Text = resp.json()['predictions']
            else:
                print(f"Missing predictions: {resp.json()}")
                print(f"Request: {batch.to_json()}")

            predictions: pd.DataFrame = pd.read_json(preds_json)
            # Take just columns: fid and predictions
            pred_columns: List[Text] = [
                'fid',
                'predictions'
            ]
            predictions = predictions[pred_columns].reset_index(drop=True)
            logging.info(f'Predictions for {model_name}:\n{predictions}')

        else:
            # Check if 'error_msg' key is present in the response
            if 'error_msg' in resp.json():
                error_msg: Text = resp.json()['error_msg']
                logging.info(f'Error: {error_msg}')
            else:
                logging.info(f'Error: Unexpected response from the server: {resp.json()}')

        total_rows_taken = end_row



if __name__ == "__main__":
    # Check if model_name is provided as a command-line argument
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    else:
        model_name = 'xgboost_model'  # Default model_name if not provided

    simulate(model_name)