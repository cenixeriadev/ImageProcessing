from confluent_kafka.admin import AdminClient, NewTopic
import os
import logging
logger = logging.getLogger(__name__)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "image-transform-requests")

def create_kafka_topic():
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BROKER})
    
    topic_list = [NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)]
    result = admin_client.create_topics(topic_list)

    for topic, f in result.items():
        try:
            f.result()  # Espera que se cree
            logging.info(f"✅ Topic creado: {topic}")
        except Exception as e:
            if "Topic already exists" in str(e):
                logging.warning(f"⚠️ Topic ya existe: {topic}")
            else:
                logging.error(f"❌ Error al crear topic {topic}: {e}")
