from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes import images

import logging
from app.services.kafka_setup import create_kafka_topic
from app.services.storage import ensure_bucket_exists


def setup_logging():
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Consola
            logging.FileHandler("app.log")  # Archivo (opcional)
        ]
    )
    # Mensaje de prueba
    logging.getLogger().info("Logging configurado")


setup_logging()    
app = FastAPI()

@app.on_event("startup")
def setup_kafka():#Crear el topic de Kafka al iniciar la app y solo si no existe
    create_kafka_topic()
    ensure_bucket_exists()
    
    
app.include_router(auth.router)
app.include_router(images.router)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
