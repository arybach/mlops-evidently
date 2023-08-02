import sys
import os

# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

import joblib
import pandas as pd
from src.utils.predictions import prepare_scoring_data
from pathlib import Path
import boto3

def fetch_models_from_s3(model_names):
    """Fetch models from S3 and save them in the 'models' directory."""
    s3_bucket_name = "mlops-nutrients"  # Replace with your S3 bucket name
    s3_client = boto3.client('s3')

    # List the model files in S3
    model_files = [ f"{model_name}.joblib" for model_name in model_names ]

    # Create the 'models' directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    # Fetch models from S3 and save them in the 'models' directory
    for model_file in model_files:
        s3_object_key = f"models/{model_file}"
        local_model_path = models_dir / model_file
        s3_client.download_file(s3_bucket_name, s3_object_key, str(local_model_path))
        print(f"Model '{model_file}' downloaded from S3 and saved in 'models' directory.")

def prepare_reference_dataset(model_name):
    """Prepare reference dataset for the monitoring."""
    DATA_FEATURES_DIR = "data/features"
    REFERENCE_DATA_DIR = Path("data/reference")
    REFERENCE_DATA_DIR.mkdir(parents=True, exist_ok=True)  # Create all parent directories if they don't exist

    target_col = "score"
    prediction_col = "predictions"

    print("Load validation data")
    path = f"{DATA_FEATURES_DIR}/validation_data.parquet"
    data = pd.read_parquet(path)
    data = data.sample(frac=0.5)

    scoring_data = prepare_scoring_data(data)

    print("Load model")
    model_path = Path("models") / f"{model_name}.joblib"
    model = joblib.load(model_path)

    # Generate Predictions
    predictions_df = data.loc[:, ["fid", target_col]]
    predictions_df[prediction_col] = model.predict(scoring_data)
   
    # concat dfs before writing
    df = pd.concat([predictions_df, scoring_data], axis=1)

    # Save Reference Dataset
    path = REFERENCE_DATA_DIR / f"{model_name}/validation_data.parquet"
    os.makedirs(f"{REFERENCE_DATA_DIR}/{model_name}", exist_ok=True)
    df.to_parquet(path)

    print("Validation Data:")
    print(df.head())  # Print the head() of the validation dataset with predictions

    print("Load testing data")
    path = f"{DATA_FEATURES_DIR}/testing_data.parquet"
    os.makedirs(f"{DATA_FEATURES_DIR}", exist_ok=True)
    data = pd.read_parquet(path)
    data = data.sample(frac=0.5)

    scoring_data = prepare_scoring_data(data)

    # Generate Predictions
    predictions_df = data.loc[:, ["fid", target_col]]
    predictions_df[prediction_col] = model.predict(scoring_data)

    # Merge DataFrames based on 'fid' column, including only matching rows
    df = pd.concat([predictions_df, scoring_data], axis=1)

    # Save Reference Dataset
    path = REFERENCE_DATA_DIR / f"{model_name}/testing_data.parquet"
    os.makedirs(f"{REFERENCE_DATA_DIR}/{model_name}", exist_ok=True)
    df.to_parquet(path)

    print("Testing Data:")
    print(df.head())  # Print the head() of the validation dataset with predictions

if __name__ == "__main__":
    # Prepare reference dataset for each model
    model_names = [ 
                    "linear_regression_model",
                    "xgboost_model"
                ]  

    # Fetch models from S3 and save them in the 'models' directory
    fetch_models_from_s3(model_names)

    for model_name in model_names:
        prepare_reference_dataset(model_name)
