import csv
import json
import time
import argparse
import paho.mqtt.client as mqtt


def publish_data(input_file, broker, port, topic, interval):
    client = mqtt.Client()
    client.connect(broker, port)
    print(f"Connected to MQTT broker at {broker}:{port}")

    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payload = {
                "timestamp": time.time(),
                "vehicle_id": row.get("vehicle_id", "veh-001"),
                "trip_id": row.get("trip_id", "trip-001"),
                "latitude": float(row.get("latitude", 0.0)),
                "longitude": float(row.get("longitude", 0.0)),
                "speed_kph": float(row.get("speed_kph", 0.0)),
                "fuel_level": float(row.get("fuel_level", 0.0)),
                "aux_power_kw": float(row.get("aux_power_kw", 0.0))
            }

            client.publish(topic, json.dumps(payload))
            print(f"Published: {json.dumps(payload)}")
            time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate vehicle telemetry over MQTT.")
    parser.add_argument("--input", required=True, help="Path to VED CSV file")
    parser.add_argument("--broker", default="localhost", help="MQTT broker hostname")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic", default="vehicle/telemetry", help="MQTT topic to publish to")
    parser.add_argument("--interval", type=float, default=0.5, help="Delay between messages in seconds")

    args = parser.parse_args()
    publish_data(args.input, args.broker, args.port, args.topic, args.interval)
