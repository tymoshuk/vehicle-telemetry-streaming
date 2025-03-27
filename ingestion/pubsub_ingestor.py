import json
import paho.mqtt.client as mqtt
from google.cloud import pubsub_v1
import os
import logging

# --- Config ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "vehicle/telemetry"

PUBSUB_TOPIC = "vehicle-telemetry-raw"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")  # Optional override

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# --- Pub/Sub Client ---
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)


# --- MQTT Callback ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("✅ Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        logging.info(f"📥 Subscribed to topic '{MQTT_TOPIC}'")
    else:
        logging.error(f"❌ MQTT connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        # Pub/Sub expects bytes
        future = publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
        future.result()

        logging.info(f"➡️ Published to Pub/Sub: {data['vehicle_id']} @ {data['timestamp']}")
    except Exception as e:
        logging.error(f"❌ Failed to process message: {e}")


# --- MQTT Client Setup ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
logging.info("🚀 Starting MQTT → Pub/Sub bridge...")

client.loop_forever()
