import pandas as pd
from pathlib import Path
from config.config import DATA_COLUMNS
import os

def process() -> None:
    """Process the datasets for training, validation, and testing."""

    # Specify the directories for saved datasets and features
    DATA_RAW_DIR = "data/raw"
    DATA_FEATURES_DIR = "data/features"

    # Define the filenames for training, validation, and testing datasets
    training_file = "training_data.parquet"
    validation_file = "validation_data.parquet"
    testing_file = "testing_data.parquet"

    # Read the training dataset from the saved Parquet file
    training_path = Path(DATA_RAW_DIR) / training_file
    training_data = pd.read_parquet(training_path)

    # Read the validation dataset from the saved Parquet file
    validation_path = Path(DATA_RAW_DIR) / validation_file
    validation_data = pd.read_parquet(validation_path)

    # Read the testing dataset from the saved Parquet file
    testing_path = Path(DATA_RAW_DIR) / testing_file
    testing_data = pd.read_parquet(testing_path)

    # Define numerical features used for training
    numerical_features = DATA_COLUMNS.num_features

    # Process each dataset (training, validation, and testing)
    for dataset, file in zip([training_data, validation_data, testing_data],
                             [training_file, validation_file, testing_file]):
        print(f"Processing {file}")

        # Drop columns 'description' and 'embeddings' if they exist
        dataset = dataset.drop(["description", "embeddings"], axis=1, errors='ignore')
        # dataset["uuid"] = [uuid.uuid4() for x in range(len(dataset))]
        # dataset["uuid"] = dataset["uuid"].astype("str")

        # Ensure all numerical features exist in the dataset and fill missing values with 0
        for feature in numerical_features:
            if feature not in dataset.columns:
                dataset[feature] = 0

        # Ensure 'score' is present in the dataset and fill missing values with 0
        if 'score' not in dataset.columns:
            dataset['score'] = 0

        # Save the processed dataset
        processed_path = Path(DATA_FEATURES_DIR) / file
        os.makedirs(f"{DATA_FEATURES_DIR}", exist_ok=True)
        dataset.to_parquet(processed_path, index=False)

if __name__ == "__main__":
    process()
