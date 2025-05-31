from worker.kafka_consumer import run_consumer
import logging
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

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    setup_logging()
    logger.info("Worker service is starting...")
    run_consumer()
    
