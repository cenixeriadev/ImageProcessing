import io
import uuid
from PIL import Image, ImageOps
from worker.storage import download_image, upload_image
import logging
logger = logging.getLogger(__name__)

def get_key(url : str)->str:
    """
    Extrae la clave del objeto de una URL de MinIO.
    """
    return url.split('/')[-2] + '/' + url.split('/')[-1]
    

def process_image_task(original_key: str, transformation: dict) -> str:
    """
    Procesa una imagen aplicando transformaciones y la sube a MinIO.
    Devuelve el nuevo image_path.
    """

    #  Descargar imagen desde MinIO como objeto PIL
    key = get_key(original_key)
    logger.info(f"📥 Descargando imagen desde MinIO con key: {key}")
    image = download_image(key)

    #  Aplicar transformaciones
    if transformation.get("resize"):
        size = transformation["resize"]
        width = size.get("width")
        height = size.get("height")
        if width and height:
            logger.info(f"🔄 Redimensionando imagen a {width}x{height}")
            image = image.resize((width, height))
        else:
            logger.warning("⚠️ Redimensionamiento solicitado sin ancho o alto especificado.")

    if transformation.get("grayscale"):
        logger.info(f"🌈 Aplicando transformación a escala de grises  con {transformation.get('grayscale')}")
        image = ImageOps.grayscale(image)

    # TODO: Añadir más implementaciones

    # Guardar en memoria como bytes
    buffer = io.BytesIO()
    ext = original_key.split('.')[-1].upper()
    format = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP"
    }.get(ext, "JPEG")
    
    image.save(buffer, format=format)
    buffer.seek(0)

    # Generar nuevo path y subir
    new_key = f"transformed/{uuid.uuid4()}.{format.lower()}"
    upload_image(buffer.read(), new_key, content_type=f"image/{format.lower()}")

    return "http://localhost:9000/dev-bucket/" + new_key
