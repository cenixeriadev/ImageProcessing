from confluent_kafka import Consumer
import os
import json
from datetime import datetime
from worker.image_processor import process_image_task
from worker.database import get_session
from worker.models import ImageTask, TaskLog
import logging

logger = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "image-transform-requests")
GROUP_ID = os.getenv("KAFKA_GROUP", "image-workers")

consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([TOPIC])


def handle_task(task_data):
    db = next(get_session())
    task_id = task_data["task_id"]
    try:
        task = db.query(ImageTask).filter(ImageTask.id == task_id).first()
        if not task:
            logger.warning(f"⚠️ Tarea {task_id} no encontrada en DB.")
            return

        task.status = "processing"
        db.commit()

        # 🧠 Procesar imagen y subir resultado
        new_path = process_image_task(task_data["image_path"], task_data["transformation"])
        task.image_path = new_path
        task.status = "completed"
        task.completed_at = datetime.utcnow()

        db.add(TaskLog(task_id=task.id, log_message="Transformación completada."))
        db.commit()
        logger.info(f"✅ Tarea {task_id} completada.")
        
    except Exception as e:
        task = db.query(ImageTask).filter(ImageTask.id == task_id).first()
        if task:
            task.status = "error"
            db.add(TaskLog(task_id=task.id, log_message=f"Error: {str(e)}"))
            db.commit()
        logger.error(f"❌ Error procesando tarea {task_id}: {e}")


def run_consumer():
    logger.info("👷 Worker escuchando tareas Kafka...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Kafka error: {msg.error()}")
            continue

        try:
            task_data = json.loads(msg.value().decode("utf-8"))
            handle_task(task_data)
        except Exception as e:
            logger.error(f"❌ Error deserializando mensaje: {e}")



