from typing import BinaryIO
import boto3
from botocore.exceptions import ClientError
from catalog_conf import Minio_Settings
from dotenv import load_dotenv

load_dotenv()
env = Minio_Settings()

client_boto3 = boto3.client(
    "s3",
    endpoint_url=f"http://{env.MINIO_URL}",
    aws_access_key_id=env.MINIO_ACCESS_KEY,
    aws_secret_access_key=env.MINIO_SECRET_KEY,
    verify=False
)

BUCKET_NAME = "product"

try:
    client_boto3.head_bucket(Bucket=BUCKET_NAME)
except ClientError as e:
    if e.response['Error']['Code'] == '404':
        client_boto3.create_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' created successfully")


def upload_image_to_minio(file: BinaryIO, file_name: str) -> bool:
    try:
        client_boto3.upload_fileobj(file, BUCKET_NAME, file_name)
        print(f"Image '{file_name}' uploaded successfully")
        return True
    except Exception as err:
        print(f"Upload failed: {err}")
        return False



def get_image_from_minio(product_name: str):
    try:
        response = client_boto3.get_object(Bucket=BUCKET_NAME, Key=product_name)
        content_type = response["ContentType"]
        return response["Body"], content_type
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            print(f"Image '{product_name}' not found in bucket")
        else:
            print(f"Failed to retrieve image: {e}")
        return None, None