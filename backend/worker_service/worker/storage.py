import boto3
import os
from PIL import Image
import io
from botocore.exceptions import ClientError

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID" , "minioadmin"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY" , "minioadmin"),
    endpoint_url="http://minio:9000",  # Usar MinIO
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

BUCKET_NAME = os.getenv("BUCKET_NAME", "dev-bucket")

def download_image(key: str) -> Image.Image:
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        return Image.open(io.BytesIO(obj["Body"].read()))
    except ClientError as e:
        raise Exception(f"Error al descargar {key}: {e.response['Error']['Message']}")

def upload_image(file_bytes: bytes, key: str, content_type: str = "image/jpeg")->None:
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=file_bytes,
        ContentType=content_type
    )
