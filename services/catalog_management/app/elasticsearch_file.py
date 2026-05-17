
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

def update_product(product_id:str, product:dict):
    try:
        response = es.update(
            index=INDEX_NAME, id=product_id, doc=product)

        if response['result']=="updated":
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
        return False

def get_product_by_id(id:str):
    try:
        response = es.get(index=INDEX_NAME, id=id)
        return response
    except Exception as e:
        print(e)
        return False

def get_product_by_name(name:str):
    try:
        product = es.search(index=INDEX_NAME, query={"match": {"name": name}})
        return product["hits"]["hits"][0]
    except Exception as e:
        print(e)
        return None
    # {'took': 3, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 2.1911242, 'hits': [{'_index': 'products', '_type': '_doc', '_id': 'CbfnIZ4BHEel-3wZhBPp', '_score': 2.1911242, '_ignored': ['image_url.keyword'], '_source': {'name': 'hhhhh', 'description': 'Artisan loaf, baked fresh', 'price': 5.49, 'category': 'Bakery', 'stock_count': 10, 'image_url': 'http://minio:9000/product/no_image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20260513%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260513T151504Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=e8461134a03a74e7eb04fab46d62586323b5aeb713654c19d55f98ade2328922'}}]}}
            
            # uv run uvicorn products.products_management:app --reload