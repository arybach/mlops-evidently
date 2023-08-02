import os
from typing import Dict, Text

host: Text = os.getenv('MONITORING_DB_HOST', 'localhost')
DATABASE_URI: Text = f'postgresql://admin:admin@{host}:5432/monitoring_db'

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
es_local_host="localhost"
es_password="changeme"
