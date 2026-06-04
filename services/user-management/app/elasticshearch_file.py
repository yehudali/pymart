from elasticsearch import Elasticsearch
import os
from config import settings

class ElasticsearchClient:
    def __init__(self, host='localhost', port=9200):
        self.es = Elasticsearch(f"http://{host}:{port}")


# Initialize Elasticsearch client
host = settings.ELASTICSEARCH_HOST
port = settings.ELASTICSEARCH_PORT

elasic_instance = ElasticsearchClient(host=host, port=port)

