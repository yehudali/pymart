from elasticsearch import AsyncElasticsearch


async def save_order(elastic_client: AsyncElasticsearch, order: dict):
    try:
        response = await elastic_client.index(index="orders", document=order)
        print(response)
        return response.body

    except Exception as err:
        print(f"error whith save_order in elastic: {err}")
        raise




async def get_all_orders(elastic_client: AsyncElasticsearch) -> list:
    try:
        response = await elastic_client.search(
            index="orders", 
            query={"match_all": {}}
        )
        
        hits = response.get("hits", {}).get("hits", [])
        
        orders = []
        for hit in hits:
            order_data = hit["_source"]
            order_data["elastic_id"] = hit["_id"]  # !הוספת המזהה מאלסטיק
            orders.append(order_data)
            
        return orders

    except Exception as err:
        print(f"Error getting all orders from ElasticSearch: {err}")
        raise