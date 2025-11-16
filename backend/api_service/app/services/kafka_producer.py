from confluent_kafka import Producer
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "image-transform-requests")

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def send_transformation_task(task_data: dict):
    """
    Envia una tarea de transformación de imagen al Worker a través de Kafka.
    task_data debe incluir:
    {
        "task_id": 123,
        "user_id": 1,
        "image_path": "images/abc.jpg",
        "transformation": {...}
    }
    """
    try:
        serialized = json.dumps(task_data)
        producer.produce(TOPIC_NAME, value=serialized)
        producer.flush()  # asegura envío inmediato
        print(f"Enviado a Kafka: {task_data}")
    except Exception as e:
        print(f"Error al enviar tarea a Kafka: {e}")
        raise
