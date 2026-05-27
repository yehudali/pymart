from fastapi import APIRouter, Depends, HTTPException
from app.core.redis_client import get_redis_client
from app.core.security import checking_basic_user_permissions
from app.service.creating_orders import create_order_service



router = APIRouter()

@router.post("/create_order", tags=["orders"])
async def create_order(user_id: str = Depends(checking_basic_user_permissions), redis_client = Depends(get_redis_client)):
    """
    ראוט ליצירת הזמנה חדשה, הראוט יקבל את מזהה המשתמש שמנסה ליצור את ההזמנה, ויעביר אותו לפונקציה של יצירת ההזמנה, שתבדוק את העגלה של המשתמש ב-redis, תשלח את המוצרים והכמויות לסרוויס של הקטלוג לבדיקה האם יש מלאי זמין, במידה ויש מלאי זמין, נוכל להמשיך בתהליך יצירת ההזמנה, במידה ואין מלאי זמין, נחזיר הודעה מתאימה ללקוח שהמוצר לא זמין כרגע במלאי ולא ניתן ליצור הזמנה עם מוצר זה.
    """
    try:
        result = await create_order_service(user_id=user_id, redis_client=redis_client) # type: ignore
        if result:
            return {"success": True, "message": "Order created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Unable to create order")
        
    except Exception as err:
        print(f"error: {err}")
        raise HTTPException(status_code=500, detail=str(err))