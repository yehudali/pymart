# setup api Endpoint
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile
from elasticsearch_file import add_new_product, get_all_products, update_product, delete_product, get_product_by_id, get_product_by_name
from elasticsearch_file import elasticsearch_helthchack

router = APIRouter()


@router.get("/health")
async def health_check():
    elastic_response = elasticsearch_helthchack()
    if not elastic_response:
        raise HTTPException(status_code=500, detail="elasticsherch not return successful response")
    return {"elasticsearch is connected?": elastic_response}