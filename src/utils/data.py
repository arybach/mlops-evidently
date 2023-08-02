import sys
import os

# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

import pandas as pd
from sqlalchemy import create_engine, select
from typing import List, Text

from config.config import DATABASE_URI
from src.utils.models import XGBoostPredictionTable, LinearRegressionPredictionTable


def load_current_data(window_size: int, model_name: str) -> pd.DataFrame:
    engine = create_engine(DATABASE_URI)
    # id is autoincremented, so desc - for most recent on top
    if model_name == 'xgboost_model':
        with engine.connect() as db_connection:
            order = XGBoostPredictionTable.id.desc()
            query = (
                select(XGBoostPredictionTable).order_by(order)
                                    .limit(window_size)
            )
            current_data: pd.DataFrame = pd.read_sql_query(
                sql=query,
                con=db_connection
            )
    elif model_name == 'linear_regression_model':
        with engine.connect() as db_connection:
            order = LinearRegressionPredictionTable.id.desc()
            query = (
                select(LinearRegressionPredictionTable).order_by(order)
                                    .limit(window_size)
            )
            current_data: pd.DataFrame = pd.read_sql_query(
                sql=query,
                con=db_connection
            )

    # Check if the 'id' column exists before dropping it
    # if 'id' in current_data.columns:
    #    current_data.drop('id', axis=1, inplace=True)

    return current_data


def load_reference_data(columns: List[Text], model_name: str) -> pd.DataFrame:

    DATA_REF_DIR = "data/reference"
    ref_path = f"{DATA_REF_DIR}/{model_name}/testing_data.parquet"
    ref_data = pd.read_parquet(ref_path)
    reference_data = ref_data.loc[:, columns]
    return reference_data
