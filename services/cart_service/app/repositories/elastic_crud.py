from elasticsearch import AsyncElasticsearch


async def is_product_exists_in_elastic(
    elastic_client: AsyncElasticsearch, product_id: str
) -> bool:
    try:
        product_exists = await elastic_client.exists(index="products", id=product_id)
        return product_exists.body

    except Exception as err:
        print(f"error: {err}")
        return False
