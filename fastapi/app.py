import sys
import os
# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

import logging
from typing import Callable, Text

from evidently import ColumnMapping
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    Response,
    FileResponse
)
from pydantic import BaseModel
import pandas as pd

from config.config import DATA_COLUMNS
from src.utils.data import load_current_data, load_reference_data
from src.utils.predictions import get_predictions, save_predictions
from src.utils.reports import (
    get_column_mapping,
    build_model_performance_report,
    build_target_drift_report
)
from utils import ModelLoader

logging.basicConfig(
    level=logging.INFO,
    format='FASTAPI_APP - %(asctime)s - %(levelname)s - %(message)s'
)

class Features(BaseModel):
    """Features model."""
    features: Text

app = FastAPI()

@app.get('/')
def index() -> HTMLResponse:
    return HTMLResponse('<h1><i>Evidently + FastAPI</i></h1>')

@app.post('/predict/{model_name}')
def predict(
    model_name: str,
    response: Response,
    features_item: Features,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    try:
        # Receive features item and read features batch
        features: pd.DataFrame = pd.read_json(features_item.features)
        # Get the corresponding model based on the specified model_name
        model_loader = ModelLoader(model_name=model_name)
        # Get the corresponding model based on the specified model_name
        model: Callable = model_loader.get_model()
        
        # Compute predictions using the selected model
        predictions = get_predictions(features, model) # all columns
        features['predictions'] = predictions['predictions'] # update just the predictions column
        print(f"Received JSON: {features_item.features}")

        # Save predictions to database (in the background)
        background_tasks.add_task(save_predictions, predictions, model_name)
        # Return JSON with predictions dataframe serialized to JSON string
        print(f"Response JSON: {features.to_json()}")

        return JSONResponse(content={'predictions': features.to_json()})
    except Exception as e:
        response.status_code = 500
        logging.error(e, exc_info=True)
        return JSONResponse(content={'error_msg': str(e)})


@app.get('/monitor-model/{model_name}')
def monitor_model_performance(model_name: str, window_size: int = 3000) -> FileResponse:

    logging.info('Read current data')
    current_data: pd.DataFrame = load_current_data(window_size, model_name=model_name)

    logging.info('Read reference data')
    reference_data = load_reference_data(columns=DATA_COLUMNS['columns'], model_name=model_name)

    logging.info('Build report')
    column_mapping: ColumnMapping = get_column_mapping(**DATA_COLUMNS)
    report_path: Text = build_model_performance_report(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
        model_name=model_name
    )

    logging.info('Return report as html')
    return FileResponse(report_path)


@app.get('/monitor-target/{model_name}')
def monitor_target_drift(model_name: str, window_size: int = 3000) -> FileResponse:

    logging.info('Read current data')
    current_data: pd.DataFrame = load_current_data(window_size, model_name=model_name)

    logging.info('Read reference data')
    reference_data = load_reference_data(columns=DATA_COLUMNS['columns'], model_name=model_name)

    logging.info('Build report')
    column_mapping: ColumnMapping = get_column_mapping(**DATA_COLUMNS)
    report_path: Text = build_target_drift_report(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
        model_name=model_name
    )

    logging.info('Return report as html')
    return FileResponse(report_path)