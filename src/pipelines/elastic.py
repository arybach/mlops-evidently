import sys
import os

# Get the absolute path to the parent directory of src (which contains config package)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

from elasticsearch import Elasticsearch
import os
import ssl
from config.config import es_local_host, es_password, es_cloud_host

def get_elastic_client(mode: str ='local'):
    # initialized local or cloud elastic search client
    # if os.environ.get(var) returns None it attempts to use the values from config.py
    # this is needed in case some of envs were not passed to the container and it takes some time to redeploy one

    ES_CLOUD_ID = os.environ.get("ES_CLOUD_ID")
    ES_USERNAME = os.environ.get("ES_USERNAME")
    ES_PASSWORD = os.environ.get("ES_PASSWORD")
    # ES_ENDPOINT = os.environ.get("ES_ENDPOINT")

    if not ES_USERNAME:
        ES_USERNAME = "elastic"

    if not ES_PASSWORD:
        ES_PASSWORD = es_password

    # Create the Elasticsearch client
    if mode == 'cloud':
        try:
            if not ES_CLOUD_ID:
                ES_CLOUD_ID = es_cloud_host

            # Connect to Elasticsearch cloud - port is not needed here
            # port = 9243        
            client = Elasticsearch(
                cloud_id=ES_CLOUD_ID,
                basic_auth=(ES_USERNAME, ES_PASSWORD)
            )
        except Exception as e:
            print(f"Failed to create Elasticsearch client in cloud mode. Error: {str(e)}")
            # this is for debugging
            #print(f"ES_USERNAME: {ES_USERNAME}")
            #print(f"ES_PASSWORD: {ES_PASSWORD}")
            raise e

    elif mode == 'local':
        try:

            port = 9200
            if es_local_host:
                local_host = es_local_host
                scheme = "https"
            else:
                local_host = "localhost"
                scheme = "http"

            # Create the Elasticsearch client
            client = Elasticsearch(
                hosts=[{"host": local_host, "port": port, "scheme": scheme}],
                basic_auth=(ES_USERNAME, ES_PASSWORD),
                verify_certs=False  # Disable certificate verification
            )
        except Exception as e:
            print(f"Failed to create local Elasticsearch client. Error: {str(e)}")
            # this is for debugging
            # print(f"ES_USERNAME: {ES_USERNAME}")
            # print(f"ES_PASSWORD: {ES_PASSWORD}")
            raise e
    else:
        client = None
    
    # if client:
        # Successful response!
        # print(client.cluster.health())
        
    return client


def drop_index(es_client, index):
    """ drop index from elastic search """
    es_client.indices.delete(index=index)
    print(f"Index '{index}' has been dropped successfully.")
