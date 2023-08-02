from typing import Text
import pandas as pd
from elasticsearch.helpers import scan
from tqdm import tqdm
from elastic import get_elastic_client

def load_data_from_elasticsearch(index_name: Text) -> dict:
    """Load data from Elasticsearch index.

    Args:
        index_name (Text): Elasticsearch index name to load data from.
        es_config (dict): Elasticsearch configuration.

    Returns:
        dict: Dictionary with three datasets: 'training', 'validation', and 'testing'.
    """
    DATA_RAW_DIR = "data/raw"

    es = get_elastic_client('local')
    scroll_size = 10000

    # Define the labels and corresponding datasets
    labels = ["training", "validation", "testing"]
    datasets = {}

    for label in labels:
        # Define the query to retrieve documents for the current label
        query = {
            "query": {
                "term": {
                    "label.keyword": label
                }
            },
            "size": scroll_size
        }

        # Use the scan function to retrieve all documents from the index
        response = scan(es, query=query, index=index_name, scroll="2m")

        data = []
        filtered_out_count = 0  # Counter to keep track of filtered out documents

        for hit in tqdm(response, desc=f"Loading {label} data", unit="docs"):
            source = hit["_source"]
            if source and source["score"] is not None:  # Filter out documents without a score
                if source["labelNutrients"]:
                    # using declared nutrition values
                    # Fill missing values with 0 (as it makes sense in this case)
                    fields = ["fat", "saturatedFat", "transFat", "cholesterol", "sodium", "carbohydrates", "fiber", "sugars",
                              "protein", "calcium", "iron", "potassium", "calories"]

                    item = {
                        "fid": source["fid"],
                        "description": source["description"],
                        "score": source["score"]
                    }
                    for field in fields:
                        amount = source["labelNutrients"].get(field, {"amount": 0})
                        if amount:
                            val = amount.get("amount", 0)
                        else:
                            val = 0
                        item[field] = val

                    data.append(item)

                elif source["nutrients"]:
                    # using calculated nutrition values
                    # Fill missing values with 0 (as it makes sense in this case)
                    fields = ["fat", "saturatedFat", "transFat", "cholesterol", "sodium", "carbohydrates", "fiber", "sugars",
                              "protein", "calcium", "iron", "potassium", "calories"]

                    item = {
                        "fid": source["fid"],
                        "description": source["description"],
                        "score": source["score"]
                    }
                    for field in fields:
                        amount = source["nutrients"].get(field, {"amount": 0})
                        if amount:
                            val = amount.get("amount", 0)
                        else:
                            val = 0
                        item[field] = val

                    data.append(item)
            else:
                filtered_out_count += 1

        # Convert the documents to a pandas DataFrame and assign it to the corresponding dataset
        datasets[label] = pd.DataFrame(data)

        # Save the dataset to a Parquet file
        file_path = f"{DATA_RAW_DIR}/{label}_data.parquet"
        datasets[label].to_parquet(file_path, index=False)

        # Print the count of filtered out documents for the current label
        print(f"Filtered out {filtered_out_count} documents without a score for {label} data.")

    return datasets

if __name__ == "__main__":
    # Example usage
    index_name = "labeled"  # Update with your Elasticsearch index name
    datasets = load_data_from_elasticsearch(index_name)
