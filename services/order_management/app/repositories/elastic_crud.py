from elasticsearch import AsyncElasticsearch


async def save_order(elastic_client: AsyncElasticsearch, order: dict):
    try:
        response = await elastic_client.index(index="orders", document=order)
        print(response)
        return response.body

    except Exception as err:
        print(f"error whith save_order in elastic: {err}")
        raise
