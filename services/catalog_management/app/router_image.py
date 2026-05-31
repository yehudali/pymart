# setup api Endpoint
from fastapi import APIRouter, HTTPException, UploadFile
from minio_file import upload_image_to_minio, get_image_from_minio
from fastapi.responses import StreamingResponse

router = APIRouter()

#images managment:
@router.post("/image", tags=["catalog_image"])
async def upload_image(file: UploadFile):
    try:
        is_uploaded = upload_image_to_minio(file.file, file.filename) # type: ignore
 
        if not is_uploaded:
            raise HTTPException(status_code=500, detail="Failed to upload image to minio")
 
        return {"status": "successfully uploaded", "file_name": file.filename}
 
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload image")


@router.get("/image/{product_name}", tags=["image"])
async def get_image(product_name: str):
    try:
        image_stream, content_type = get_image_from_minio(product_name)
 
        if not image_stream:
            raise HTTPException(status_code=404, detail=f"Image '{product_name}' not found")
 
        return StreamingResponse(image_stream, media_type=content_type)
 
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve image")