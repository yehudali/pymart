from fastapi import Request
from elasticsearch import AsyncElasticsearch

def get_elastic_search_client(request:Request) -> AsyncElasticsearch:
    return request.app.state.elastic_client