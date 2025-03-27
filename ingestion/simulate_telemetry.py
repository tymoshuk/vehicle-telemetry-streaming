import csv
import json
import time
from datetime import datetime, timedelta
import argparse
import paho.mqtt.client as mqtt


def _parse_nullable(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def publish_data(input_file, broker, port, topic, interval):
    client = mqtt.Client()
    client.connect(broker, port)
    print(f"Connected to MQTT broker at {broker}:{port}")

    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        base_time = datetime.utcnow()
        for row in reader:
            relative_ms = int(row.get("Timestamp(ms)", 0))
            absolute_time = base_time + timedelta(milliseconds=relative_ms)
            payload = {
                "vehicle_id": f"VEH_{row.get('VehId', '0')}",
                "trip_id": int(row.get("Trip", 0)),
                "timestamp": absolute_time.isoformat() + "Z",
                "latitude": float(row.get("Latitude[deg]", 0.0)),
                "longitude": float(row.get("Longitude[deg]", 0.0)),
                "speed_kph": float(row.get("Vehicle Speed[km/h]", 0.0)),
                "maf_gps": float(row.get("MAF[g/sec]", 0.0)),
                "engine_rpm": float(row.get("Engine RPM[RPM]", 0.0)),
                "load_pct": float(row.get("Absolute Load[%]", 0.0)),
                "oat_c": _parse_nullable(row.get("OAT[DegC]")),
                "fuel_rate_lph": _parse_nullable(row.get("Fuel Rate[L/hr]")),
                "ac_power_kw": _parse_nullable(row.get("Air Conditioning Power[kW]")),
                "ac_power_w": _parse_nullable(row.get("Air Conditioning Power[Watts]")),
                "heater_power_w": _parse_nullable(row.get("Heater Power[Watts]")),
                "hv_battery_current_a": _parse_nullable(row.get("HV Battery Current[A]")),
                "hv_battery_soc_pct": _parse_nullable(row.get("HV Battery SOC[%]")),
                "hv_battery_voltage_v": _parse_nullable(row.get("HV Battery Voltage[V]")),
                "stft_b1_pct": _parse_nullable(row.get("Short Term Fuel Trim Bank 1[%]")),
                "stft_b2_pct": _parse_nullable(row.get("Short Term Fuel Trim Bank 2[%]")),
                "ltft_b1_pct": _parse_nullable(row.get("Long Term Fuel Trim Bank 1[%]")),
                "ltft_b2_pct": _parse_nullable(row.get("Long Term Fuel Trim Bank 2[%]"))
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
