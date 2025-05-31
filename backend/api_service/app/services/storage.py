import boto3
from botocore.exceptions import NoCredentialsError
import uuid
import os
import logging
import urllib.parse as urlparse

logger = logging.getLogger(__name__)

# Variables de entorno o valores directos para MinIO
MINIO_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
MINIO_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
MINIO_ENDPOINT = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
BUCKET_NAME = os.getenv("BUCKET_NAME", "dev-bucket")
# Cliente MinIO usando boto3
s3 = boto3.client(
    's3',
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    endpoint_url=MINIO_ENDPOINT,
    region_name='us-east-1'
)

def ensure_bucket_exists():
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        logger.info(f"✅ Bucket '{BUCKET_NAME}' ya existe.")
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.info(f"📦 Bucket '{BUCKET_NAME}' no existe. Creándolo...")
            s3.create_bucket(Bucket=BUCKET_NAME)
        else:
            raise




def upload_image(file_data: bytes, original_filename: str) -> str:
    """Sube una imagen a MinIO y retorna su URL interna."""
    extension = original_filename.split('.')[-1]
    key = f"images/{uuid.uuid4()}.{extension}"

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=file_data,
            ContentType=f"image/{extension}"
        )
        # Devuelve URL directa solo válida si MinIO permite acceso público
        return f"http://localhost:9000/{BUCKET_NAME}/{key}"
    except NoCredentialsError:
        raise Exception("Credenciales de MinIO no configuradas correctamente.")

def delete_image(file_url: str):
    """Elimina una imagen del bucket usando su URL."""
    parsed = urlparse(file_url)
    key = '/'.join(parsed.path.split('/')[2:])  # quitar el bucket del path

    s3.delete_object(Bucket=BUCKET_NAME, Key=key)