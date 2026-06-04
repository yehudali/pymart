from elasticsearch import AsyncElasticsearch
import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException

# from app.repositories.redis_crud import get_item
from app.service.cart_crud import (
    add_or_update_product_to_user_cart,
    delete_product_from_cart1,
    delete_cart1,
    update_quantity1,
    get_cart_product_and_information,
    is_product_exists_in_catalog,
)
from app.core.redis_client import get_redis_client
from app.core.elasticsearch_client import get_elastic_client
from app.core.security import checking_basic_user_permissions
from app.schemas.product import (
    AddProductToCart,
    DeleteProduct,
    UpdateQuantityProduct,
    CreateItemDTO,
)
from app.schemas.cart import CartInfoResponse

router = APIRouter()


@router.get("/healthcheck", tags=["healthcheck"])
async def healthcheck_test(redis_client: redis.Redis = Depends(get_redis_client)):
    """Checking if there is a connection to the REDIS server, returning a boolean response"""
    return await redis_client.ping()  # type: ignore


@router.post("/cart/product", tags=["cart"])
async def add_product_to_cart(
    product: AddProductToCart,
    elastic_client: AsyncElasticsearch = Depends(get_elastic_client),
    user_id=Depends(checking_basic_user_permissions),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    """בדיקה וחיבור לאלסטיק, בכדי לוודאות לפני ההוספה שהמוצר קיים בקטלוג"""
    try:
        product_exists = await is_product_exists_in_catalog(
            product_id=product.id, elastic_client=elastic_client
        )
        if not product_exists:
            raise HTTPException(
                status_code=404, detail="product not found in the catalog!"
            )
    except Exception as err:
        print(f"error: {err}")
        raise HTTPException(
            status_code=404,
            detail="error while checking product in the catalog, show logs",
        )

    """הוספה או עדכון של מוצר בעגלה, במידה והמוצר כבר קיים בעגלה, הוא יעודכן עם הכמות החדשה בלבד! בלי עדכון מחיר שם.. וכדומה"""
    try:
        product_data = CreateItemDTO(
            name=product.name, price=product.price, quantity=product.quantity
        )
        return await add_or_update_product_to_user_cart(
            user_id=user_id,
            product_id=product.id,
            data=product_data,
            redis_client=redis_client,
        )
    except Exception as err:
        print(f"error: {err}")
        raise HTTPException(status_code=500, detail="something went wrong show logs")


@router.delete("/cart/product", tags=["cart"])
async def delete_product_from_cart(
    product_id: DeleteProduct,
    user_id=Depends(checking_basic_user_permissions),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    try:
        return await delete_product_from_cart1(
            user_id=user_id, product_id=product_id.id, redis_client=redis_client
        )
    except Exception as err:
        print(f"error: {err}")
        raise HTTPException(status_code=500, detail="something went wrong show logs")


@router.delete("/cart", tags=["cart"])
async def delete_cart(
    user_id=Depends(checking_basic_user_permissions),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    try:
        return await delete_cart1(user_id=user_id, redis_client=redis_client)
    except Exception as err:
        print(f"error: {err}")
        raise HTTPException(status_code=500, detail="something went wrong show logs")


@router.put("/cart/product/quantity", tags=["cart"])
async def update_quantity(
    update: UpdateQuantityProduct,
    user_id=Depends(checking_basic_user_permissions),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    try:
        return await update_quantity1(
            user_id=user_id,
            product_id=update.product_id,
            quantity=update.quantity,
            redis_client=redis_client,
        )
    except Exception as err:
        print(f"error: {err}")
        raise HTTPException(status_code=500, detail="something went wrong show logs")


@router.get("/cart", response_model=CartInfoResponse, tags=["cart"])
async def get_cart_and_information(
    user_id=Depends(checking_basic_user_permissions),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    try:
        return await get_cart_product_and_information(
            user_id=user_id, redis_client=redis_client
        )
    except Exception as err:
        print(f"error: {err}")
        return HTTPException(status_code=500, detail="somthin went worng show logs")
