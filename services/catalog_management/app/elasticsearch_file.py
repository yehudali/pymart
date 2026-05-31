from elasticsearch import Elasticsearch
from catalog_conf import ElasticSettings

# -> https://elasticsearch:9200

es = Elasticsearch(ElasticSettings.ELASTICSEARCH_URL)
INDEX_NAME = "products"


def elasticsearch_helthchack():
    print("dhe-url:", ElasticSettings.ELASTICSEARCH_URL)
    return es.ping()


def add_new_product(product: dict):
    try:
        response = es.index(index=INDEX_NAME, document=product)
        return response["_id"]

    except Exception as e:
        print(e)
        return False


def update_product(product_id: str, product: dict):
    try:
        response = es.update(index=INDEX_NAME, id=product_id, doc=product)

        if response["result"] == "updated":
            print(response)
            print(es.get(index=INDEX_NAME, id=product_id))
            return True
        else:
            print(response)
            return False

    except Exception as e:
        print(e)
        return False


def delete_product(product_id: str):
    try:
        response = es.delete(index=INDEX_NAME, id=product_id)
        return response
    except Exception as e:
        print(e)
        return False


def get_all_products():
    try:
        product = es.search(index=INDEX_NAME, query={"match_all": {}})
        return product
    except Exception as e:
        print(e)
        return False


def get_product_by_id(id: str):
    try:
        response = es.get(index=INDEX_NAME, id=id)
        return response
    except Exception as e:
        print(e)
        return False


def get_product_by_name(name: str):
    try:
        product = es.search(index=INDEX_NAME, query={"match": {"name": name}})
        return product["hits"]["hits"][0]
    except Exception as e:
        print(e)
        return None
