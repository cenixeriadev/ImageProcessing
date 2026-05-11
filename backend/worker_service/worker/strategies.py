from abc import ABC, abstractmethod
from PIL import Image, ImageOps
import logging

logger = logging.getLogger(__name__)


class TransformationStrategy(ABC):
    @abstractmethod
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        pass


class ResizeStrategy(TransformationStrategy):
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        width = params.get("width")
        height = params.get("height")
        if width and height:
            logger.info(f"Redimensionando imagen a {width}x{height}")
            return image.resize((width, height))
        logger.warning("Redimensionamiento solicitado sin ancho o alto especificado.")
        return image


class GrayscaleStrategy(TransformationStrategy):
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        logger.info("Aplicando transformación a escala de grises")
        return ImageOps.grayscale(image)


class MirrorStrategy(TransformationStrategy):
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        logger.info("Aplicando transformación de espejo")
        return ImageOps.mirror(image)


class FlipStrategy(TransformationStrategy):
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        logger.info("Aplicando transformación de volteo")
        return ImageOps.flip(image)


class RotateStrategy(TransformationStrategy):
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        angle = params.get("angle", 0)
        logger.info(f"Rotando imagen {angle} grados")
        return image.rotate(angle, expand=True)


class CropStrategy(TransformationStrategy):
    def apply(self, image: Image.Image, params: dict) -> Image.Image:
        x = params.get("x", 0)
        y = params.get("y", 0)
        width = params.get("width")
        height = params.get("height")
        
        if width is not None and height is not None:
            logger.info(f"Recortando imagen desde ({x},{y}) con dimensiones {width}x{height}")
            right = x + width
            bottom = y + height
            return image.crop((x, y, right, bottom))
        logger.warning("Recorte solicitado sin dimensiones especificadas.")
        return image


class ImageTransformationContext:
    def __init__(self):
        self._strategies = {
            "resize": ResizeStrategy(),
            "grayscale": GrayscaleStrategy(),
            "mirror": MirrorStrategy(),
            "flip": FlipStrategy(),
            "rotate": RotateStrategy(),
            "crop": CropStrategy(),
        }
    
    def apply_transformation(self, image: Image.Image, transformation: dict) -> Image.Image:
        result = image
        for transform_type, params in transformation.items():
            strategy = self._strategies.get(transform_type)
            if strategy:
                result = strategy.apply(result, params or {})
            else:
                logger.warning(f"Estrategia '{transform_type}' no implementada.")
        return result