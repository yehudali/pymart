# setup api Endpoint
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, Depends, Header, Request
from schemas import InsertProduct, ResponseProduce, UpdateProduct
from elasticsearch_file import add_new_product, get_all_products, update_product, delete_product, get_product_by_id, get_product_by_name

# from depends_func import get_current_user
from depends_func import get_user, SECRET_KEY

router = APIRouter()
fastapi_order_tag = ["orders"]


@router.post("/product/", tags=fastapi_order_tag)
async def add_new_product_to_elastic(product:InsertProduct, token = Depends(get_user)): # , user = Depends(get_current_user)
    product_id = add_new_product(product.model_dump())
    if product_id:
        return {"product_id": product_id, "status": f"created successfully"}
    else:
        return {"status": "failed to create product"}


@router.put("/product/{id}", tags=fastapi_order_tag)
async def update_elastic_product(product:UpdateProduct, id:str, token = Depends(get_user)):
    response = update_product(product=product.model_dump(exclude_unset=True), product_id=id)
    if response == True:
        return {"status":"successfully updated!"}
    else:
        return response


@router.delete("/product/{id}", tags=fastapi_order_tag)
async def delete_elastic_product(id, token = Depends(get_user)):
    re = delete_product(id)
    if not re:
        raise HTTPException(status_code=404, detail="product not found in elastic")
    else:
        return {"status": "successfully deleted!"}
    



@router.get("/product/{id}", tags=fastapi_order_tag)
async def get_product_from_elastic_by_id(id, token = Depends(get_user)):
    respons = get_product_by_id(id)
    if not respons:
        raise HTTPException(status_code=404, detail="product not found in elastic")
    else:
        return respons
    

@router.get("/product/", tags=fastapi_order_tag, response_model=List[ResponseProduce])
async def get_all_product_from_elastic(token = Depends(get_user)):
    try:
        product_info = get_all_products()
        products_hits = product_info["hits"]["hits"]
        return products_hits
    except Exception as e:
        print(e)
        return []

