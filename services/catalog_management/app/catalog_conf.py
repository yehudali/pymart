import os

class ElasticSettings():
    ELASTICSEARCH_URL =  os.getenv("ELASTICSEARCH_URL")

class Minio_Settings():
    MINIO_URL = os.getenv("MINIO_URL")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
