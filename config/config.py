import os
from typing import Dict, Text

# Check if .env file exists before loading the environment variables
if os.path.isfile(".env"):
    import dotenv
    dotenv.load_dotenv(".env")

host: Text = os.getenv('MONITORING_DB_HOST', 'localhost')
database_user: Text = os.getenv('POSTGRES_USER', 'admin')
database_password: Text = os.getenv('POSTGRES_PASSWORD', 'admin')

# Use the environment variables to construct the DATABASE_URI
DATABASE_URI: Text = f'postgresql://{database_user}:{database_password}@{host}:5432/monitoring_db'

# order of columns in num_features is important for linear regression model
DATA_COLUMNS: Dict = {
    'target_col': 'score',
    'prediction_col': 'predictions',
    'num_features': [
        "fat", "saturatedFat", "transFat", "cholesterol", "sodium",
        "carbohydrates", "fiber", "sugars", "protein", "calcium",
        "iron", "potassium", "calories"
    ],
    'cat_features': []
}
DATA_COLUMNS['columns'] = (
    DATA_COLUMNS['num_features'] +
    DATA_COLUMNS['cat_features'] +
    [DATA_COLUMNS['target_col'], DATA_COLUMNS['prediction_col']]
)

bucket_name='mlops-nutrients'
index='nutrients'
# model from hugging face used for vector embeddings - if any 
model="msmarco"
# set to ip address of ec2 instance created in mlops-infra/ec2
es_local_host=os.environ.get("ES_LOCAL_HOST")
es_cloud_host=''
es_password=os.environ.get("ES_PASSWORD")
