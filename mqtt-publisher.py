import json, time
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883)

with open("openxc-data/2013-07-22-10-00-00.json") as f:
    for line in f:
        msg = json.loads(line)
        payload = {
            "timestamp": msg["timestamp"],
            msg["name"]: msg["value"]
        }
        client.publish("vehicle/telemetry", json.dumps(payload))
        time.sleep(0.1)  # Simulate 10Hz streaming