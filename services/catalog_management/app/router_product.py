# setup api Endpoint
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, Depends, Header

from schemas import InsertProduct, ResponseProduce, UpdateProduct
from elasticsearch_file import add_new_product, get_all_products, update_product, delete_product, get_product_by_id, get_product_by_name


router = APIRouter()
fastapi_order_tag = ["orders"]


    

@router.post("/product/", tags=fastapi_order_tag)
async def add_new_product_to_elastic(product:InsertProduct ): # , user = Depends(get_current_user)
    product_id = add_new_product(product.model_dump())
    if product_id:
        return {"product_id": product_id, "status": f"created successfully"}
    else:
        return {"status": "failed to create product"}


@router.put("/product/{id}", tags=fastapi_order_tag)
async def update_elastic_product(product:UpdateProduct, id:str):
    response = update_product(product=product.model_dump(exclude_unset=True), product_id=id)
    if response == True:
        return {"status":"successfully updated!"}
    else:
        return response


@router.delete("/product/{id}", tags=fastapi_order_tag)
async def delete_elastic_product(id):
    return delete_product(id)


@router.get("/product/{id}", tags=fastapi_order_tag)
async def get_product_from_elastic_by_id(id):
    return get_product_by_id(id)


@router.get("/product/", tags=fastapi_order_tag, response_model=List[ResponseProduce])
async def get_all_product_from_elastic():
    try:
        product_info = get_all_products()
        products_hits = product_info["hits"]["hits"]
        return products_hits
    except Exception as e:
        print(e)
        return []

