import sys
import os

# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

import numpy as np
import pandas as pd

from config.config import DATABASE_URI, DATA_COLUMNS
from sqlalchemy import create_engine
from src.utils.db_utils import open_sqa_session
from src.utils.models import LinearRegressionPredictionTable, XGBoostPredictionTable


def prepare_scoring_data(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare scoring data.

    Args:
        data (pd.DataFrame): Input data - Pandas dataframe.

    Returns:
        pd.DataFrame: Pandas dataframe with specific features (columns).
    """

    # Define the target variable, numerical features, and categorical features
    num_features = DATA_COLUMNS['num_features']
    cat_features = DATA_COLUMNS['cat_features']
    data = data.loc[:, num_features + cat_features]

    return data


def get_predictions(data: pd.DataFrame, model) -> pd.DataFrame:
    """Predictions generation.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        model (_type_): Model object.
        model_name (str): Name of the model ('xgboost_model' or 'linear_regression_model').

    Returns:
        pd.DataFrame: Pandas dataframe with predictions column and other fields from the original dataset.
    """

    # Prepare the scoring data
    scoring_data = prepare_scoring_data(data)
    predictions = model.predict(scoring_data)

    # Add the 'predictions' column to the original DataFrame
    data['predictions'] = predictions

    return data


def save_predictions(predictions: pd.DataFrame, model_name: str) -> None:
    """Save predictions to database.

    Args:
        predictions (pd.DataFrame): Pandas dataframe with predictions column.
    """

    engine = create_engine(DATABASE_URI)
    session = open_sqa_session(engine)
    if model_name == 'xgboost_model':
        session.add_all([
            XGBoostPredictionTable(**pred) for pred in predictions.to_dict('records')
        ])
    elif model_name == 'linear_regression_model':
        session.add_all([
            LinearRegressionPredictionTable(**pred) for pred in predictions.to_dict('records')
        ])

    session.commit()
