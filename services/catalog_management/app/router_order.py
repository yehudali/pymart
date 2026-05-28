from fastapi import APIRouter, Depends, HTTPException
from typing import List
from security import checking_basic_user_permissions
from schemas import OrderItemIncoming, UpdateProduct
from elasticsearch_file import get_product_by_id, update_product

router = APIRouter()


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
    # עדכון מלאי, עם רולבאק
    successfully_updated = []

    try:
        for prod in products_to_update:
            # !עדכון המלאי החדש
            update_data = UpdateProduct(stock_count=prod["new_stock"])
            update_product(
                product=update_data.model_dump(exclude_unset=True), 
                product_id=prod["id"]
            )
            
            # תיעוד
            successfully_updated.append(prod)

    except Exception as err:

        # ביצוע הרולבאק
        print(f"Update failed halfway, Rolling back items, Error: {err}")
        for rollback_prod in successfully_updated:

            revert_data = UpdateProduct(stock_count=rollback_prod["old_stock"])
            update_product(
                product=revert_data.model_dump(exclude_unset=True), 
                product_id=rollback_prod["id"]
            )
        
        
        raise HTTPException(
            status_code=500, 
            detail="Transaction failed during stock update. No changes were saved."
        )


    # הודעת הצלחה
    return {"success": True, "message": "order validated and stock updated"}