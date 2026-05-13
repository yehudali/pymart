from typing import BinaryIO
from minio import Minio
from minio.error import S3Error
from catalog_conf import Minio_Settings
import boto3
import io
from dotenv import load_dotenv
# to run local:
load_dotenv()
env = Minio_Settings()

client = Minio(env.MINIO_URL, 
               access_key=env.MINIO_ACCESS_KEY,
                secret_key=env.MINIO_SECRET_KEY, 
                secure=False
                )

client_boto3 =boto3.client("s3",
                            endpoint_url=f"http://{env.MINIO_URL}",
                              aws_access_key_id=env.MINIO_ACCESS_KEY,
                                aws_secret_access_key=env.MINIO_SECRET_KEY,
                                verify=False)


found = client.bucket_exists("product")
if not found:
    client.make_bucket("product")
    print(F" product bucket created successfully.")

def upload_image_to_minio(file:BinaryIO, file_name:str):
    try:
        bucket_name = "product"
        client_boto3.upload_fileobj(file, bucket_name, f"{file_name}.png")
        print("the new image url is: ", get_image_url(bucket_name=bucket_name, object_name=f"{file_name}.png"))
        return {"add image": "successfully"}
    except Exception as err:
        return f"procces failed:{err}"

def get_image_url(bucket_name, object_name):
    
    try:
        if client.stat_object(bucket_name, object_name).bucket_name == bucket_name:
            print(f"'{object_name}' - picture was found in the archive")
            return client.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
        
    except S3Error:
        print(f"There is no image '{object_name}' in the archive.")
        return client.presigned_get_object(bucket_name, "no_image.png")
    ## נדרש להעלות תמונה בשם no_image.png
    ## כדי להחזיר תמונה ברירת מחדל במקרה של חוסר תמונה