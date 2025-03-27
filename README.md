# 🚗 Vehicle Telemetry Streaming Pipeline with Medallion Architecture on GCP

This project demonstrates a real-time data pipeline for ingesting vehicle sensor telemetry using the **Vehicle Energy Dataset (VED)**. The pipeline follows the **Medallion architecture** pattern on **Google Cloud Platform (GCP)**, using modern cloud-native tools to ensure scalability, data quality, and analytics readiness.

## 🧱 Architecture Overview

```
Vehicle Energy Dataset (simulated IoT) 
      ↓
MQTT Broker (EMQX)
      ↓
Kafka (Confluent Cloud)
      ↓
Dataflow (Streaming ETL, watermarking)
      ↓
GCS (Bronze Layer - raw storage)
      ↓
Cloud Function trigger on new file
      ↓
Dataproc Serverless Spark (validation + transformation)
      ↓
Delta Lake on GCS (Silver/Gold layers, schema evolution)
      ↓
Dataflow (Batch)
      ↓
BigQuery (BI-ready analytics)
      ↓
Looker Dashboards
```

## 🗃️ Dataset: Vehicle Energy Dataset (VED)

- Source: [gsoh/VED on GitHub](https://github.com/gsoh/VED)
- Format: CSV
- Contains:
  - Timestamped GPS and energy/fuel data
  - Speed, fuel level, auxiliary power, trip ID, etc.
- Simulates real-time vehicle telemetry for energy efficiency tracking.

## 📦 GCP Services Used

| Service                | Purpose                                  |
|------------------------|------------------------------------------|
| **Compute Engine / GKE** | Hosts MQTT broker (EMQX)               |
| **Kafka**              | Buffering and event bus (Confluent)   |
| **Cloud Dataflow**     | Streaming ingestion + watermarking       |
| **Cloud Storage (GCS)**| Raw data lake storage (Bronze layer)     |
| **Cloud Functions**    | Triggers Delta ETL jobs on new file arrival |
| **Dataproc Serverless**| Spark jobs for Silver/Gold Delta Lake ETL |
| **Delta Lake**         | ACID-compliant data layers (Silver/Gold) |
| **Dataproc Metastore** | Schema registration and catalog          |
| **BigQuery**           | BI-ready warehouse                       |
| **Looker**             | Data visualization & reporting           |

## 🧪 Medallion Architecture Layers

### 🥉 Bronze Layer (Raw)
- Data is written as-is from Kafka to GCS
- Format: JSON
- No transformations or filtering applied
- Partitioned by `event_time`

### 🥈 Silver Layer (Validated & Cleaned)
- Spark job triggered by Cloud Function
- Performs:
  - Schema validation
  - Required field checks
  - Type coercion
  - Time parsing
- Written as **Delta Lake** format to GCS
- Registered in **Dataproc Metastore**

### 🥇 Gold Layer (Curated & Aggregated)
- Optional second Spark job
- Aggregates trip-level KPIs
- Calculates metrics like average speed, fuel efficiency
- Output to **Delta Lake** and synced to **BigQuery**

## 🧠 Streaming Concepts Used

- **Watermarks** for late data handling
- **Tumbling windows** for time-based aggregations
- **Schema evolution** via Delta Lake auto-merge
- **Time travel** support for regulatory audits

## 🛠 Technologies

- `paho-mqtt` to simulate vehicle sensor messages
- EMQX MQTT broker
- Apache Kafka (Confluent Cloud)
- Apache Beam (via Cloud Dataflow)
- Apache Spark (Dataproc Serverless)
- Delta Lake (on GCS)
- Dataproc Metastore (Hive-compatible schema registry)
- BigQuery + Looker

## 🚀 How to Run

1. Run MQTT broker:
    ```bash
    docker run -it -p 1883:1883 \
      -v "$(pwd)/ingestion/mqtt_broker/mosquitto.conf:/mosquitto/config/mosquitto.conf" \
      eclipse-mosquitto
    ```
2. Simulate MQTT messages from VED dataset:
    ```bash
    python3 ingestion/simulate_telemetry.py --input <FILE_PATH>
    ```

## 📊 Sample KPIs in Looker

- Average fuel efficiency per trip
- Speed profiles over time
- Idle time vs drive time ratio
- Energy loss across sessions

## 🧠 Why This Matters

This architecture is inspired by real-world use cases in:
- Fleet management
- Smart mobility
- EV energy optimization
- Automotive telemetry and analytics

It follows best practices in:
- **GCP data architecture**
- **Delta Lake schema governance**
- **Streaming analytics**
- **Serverless orchestration**

## 📂 License & Credits

- Dataset: [Vehicle Energy Dataset (VED)](https://github.com/gsoh/VED) – MIT License
- Inspired by the Medallion architecture (Databricks)