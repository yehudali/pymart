from fastapi import Request
from elasticsearch import AsyncElasticsearch

async def get_elastic_client(request: Request) -> AsyncElasticsearch:
    return await request.app.state.elastic_client