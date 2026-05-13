from elasticsearch import Elasticsearch
import os
class ElasticsearchClient:
    def __init__(self, host='localhost', port=9200):
        self.es = Elasticsearch(f"http://{host}:{port}")





host = os.getenv("ELASTICSEARCH_HOST")
port = int(os.getenv("ELASTICSEARCH_PORT", 9200))
elasic_instance = ElasticsearchClient(host=host, port=port)

