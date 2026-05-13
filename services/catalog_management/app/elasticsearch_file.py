
from elasticsearch import Elasticsearch
from catalog_conf import ElasticSettings

#-> https://elasticsearch:9200

es = Elasticsearch(ElasticSettings.ELASTICSEARCH_URL)
INDEX_NAME = "products"


def elasticsearch_helthchack():
    print("dhe-url:", ElasticSettings.ELASTICSEARCH_URL)
    return es.ping()

def add_new_product(product:dict):
    try:
        response = es.index(
            index=INDEX_NAME,
            document=product
            )
        return response['_id']

    except Exception as e:
        print(e)
        return False

def update_product(product:dict, product_id:str):
    try:
        respons = es.update(
            index=INDEX_NAME, id=product_id, doc=product)

        if respons['result']=="updated":
            return True
        else:
            return respons
        
    except Exception as e:
        print(e)
        return False


def delete_product(product_id: str):
    try:
        response =  es.delete(index=INDEX_NAME, id=product_id)
        return response
    except Exception as e:
        print(e)
        return False
    
def get_all_products():
    try:
        product = es.search(index=INDEX_NAME,query={"match_all": {}})
        return product
    except Exception as e:
        print(e)
        return {"status":"False"}

def get_product_by_id(id:str):
    try:
        response = es.get(index=INDEX_NAME, id=id)
        return response
    except Exception as e:
        print(e)
        return {"status":"False"}

def get_product_by_name(name:str):
    try:
        response = es.search(index=INDEX_NAME, query={"match": {"name": name}})
        return response
    except Exception as e:
        print(e)
        return {"status":"False"}
            
            # uv run uvicorn products.products_management:app --reload