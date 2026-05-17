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
                            endpoint_url=f"http://host.docker.internal:9000",
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
        client_boto3.upload_fileobj(file, bucket_name, file_name)
        print("the new image url is: ", get_image_url(bucket_name=bucket_name, object_name=f"{file_name}.png"))
        return {"add image": "successfully"}
    except Exception as err:
        print(f"procces failed:{err}")
        return False

# def get_image_url(bucket_name, object_name):
#     try:
#         if client.stat_object(bucket_name, object_name).bucket_name == bucket_name:
#             print(f"'{object_name}' - picture was found in the archive!")
#             print((type(bucket_name)), type(object_name))
        
#             return client.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
            
        
#     except Exception as e: 
#         print(f"The actual error is: {e}")
#         print(f"Error type: {type(e)}")
#         return False
def get_image_url(bucket_name, object_name):
    try:
        image_url = client.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
        print(f"The image url is: {image_url}")
        return image_url
    
    except Exception as e:
        print(f"The actual error is: {e}")
        return False