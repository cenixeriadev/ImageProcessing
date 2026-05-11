import io
import uuid
from PIL import Image
from worker.storage import download_image, upload_image
from worker.strategies import ImageTransformationContext
import logging

logger = logging.getLogger(__name__)


def get_key(url: str) -> str:
    return url.split('/')[-2] + '/' + url.split('/')[-1]


def process_image_task(original_key: str, transformation: dict) -> str:
    key = get_key(original_key)
    logger.info(f"Descargando imagen desde MinIO con key: {key}")
    image = download_image(key)

    context = ImageTransformationContext()
    image = context.apply_transformation(image, transformation)

    buffer = io.BytesIO()
    ext = original_key.split('.')[-1].upper()
    img_format = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP"
    }.get(ext, "JPEG")

    image.save(buffer, format=img_format)
    buffer.seek(0)

    new_key = f"transformed/{uuid.uuid4()}.{img_format.lower()}"
    upload_image(buffer.read(), new_key, content_type=f"image/{img_format.lower()}")

    return "http://localhost:9000/dev-bucket/" + new_key
