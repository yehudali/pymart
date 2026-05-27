# setup api Endpoint
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, Depends, Header, Request
from schemas import InsertProduct, OrderItemIncoming, ResponseProduce, UpdateProduct
from elasticsearch_file import add_new_product, get_all_products, update_product, delete_product, get_product_by_id, get_product_by_name

from security import checking_basic_user_permissions,check_if_is_admin_user, SECRET_KEY

router = APIRouter()
fastapi_order_tag = ["orders"]


@router.post("/product/", tags=fastapi_order_tag) # type: ignore
async def add_new_product_to_elastic(product:InsertProduct, token = Depends(check_if_is_admin_user)): # , user = Depends(get_current_user)
    product_id = add_new_product(product.model_dump())
    if product_id:
        return {"product_id": product_id, "status": f"created successfully"}
    else:
        return {"status": "failed to create product"}


@router.put("/product/{id}", tags=fastapi_order_tag) # type: ignore
async def update_elastic_product(product:UpdateProduct, id:str, token = Depends(check_if_is_admin_user)):
    response = update_product(product=product.model_dump(exclude_unset=True), product_id=id)
    if response == True:
        return {"status":"successfully updated!"}
    else:
        return response


@router.delete("/product/{id}", tags=fastapi_order_tag) # type: ignore
async def delete_elastic_product(id, token = Depends(check_if_is_admin_user)):
    re = delete_product(id)
    if not re:
        raise HTTPException(status_code=404, detail="product not found in elastic")
    else:
        return {"status": "successfully deleted!"}
    



@router.get("/product/{id}", tags=fastapi_order_tag) # type: ignore
async def get_product_from_elastic_by_id(id, token = Depends(checking_basic_user_permissions)):
    respons = get_product_by_id(id)
    if not respons:
        raise HTTPException(status_code=404, detail="product not found in elastic")
    else:
        return respons
    

@router.get("/product/", tags=fastapi_order_tag, response_model=List[ResponseProduce]) # type: ignore
async def get_all_product_from_elastic():
    try:
        product_info = get_all_products()
        products_hits = product_info["hits"]["hits"]
        return products_hits
    except Exception as e:
        print(e)
        return []

@router.post("/create_order", tags=['orders'])
async def process_new_order(
    order_items: List[OrderItemIncoming], 
    token = Depends(checking_basic_user_permissions)
):
    """
    מקבל רשימה של מוצרים וכמויות. 
    בודק מלאי עבור כולם, ורק אם יש מספיק לכולם, מעדכן את המלאי.
    """
    products_to_update = []

    for item in order_items:
        product_data = get_product_by_id(item.product_id)
        
        if not product_data:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        current_stock = product_data.get("_source", {}).get("stock_count", 0)
        
        if current_stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"there is not enough stock for product {item.product_id}"
            )
        # שמירה בליסט לצורך עדכון בשלב הבא
        products_to_update.append({
            "id": item.product_id,
            "new_stock": current_stock - item.quantity
        })
    # ==========================================
    # עדכון מלאי
    for prod in products_to_update:
        update_data = UpdateProduct(stock_count= prod["new_stock"])
        
        update_product(
            product=update_data.model_dump(exclude_unset=True), product_id=prod["id"])

    return {"success": True, "message": "Order validated and stock updated"}