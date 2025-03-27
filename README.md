# 🚗 Vehicle Telemetry Streaming Pipeline with Medallion Architecture on GCP

This project demonstrates a real-time data pipeline for ingesting vehicle sensor telemetry using the **Vehicle Energy Dataset (VED)**. The pipeline follows the **Medallion architecture** pattern on **Google Cloud Platform (GCP)**, using modern cloud-native tools to ensure scalability, data quality, and analytics readiness.

## 🧱 Architecture Overview

```
Vehicle Energy Dataset (simulated IoT)  
      ↓  
MQTT Broker (Mosquitto)  
      ↓  
Pub/Sub (Buffering, decoupling layer)  
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

| Service                | Purpose                                                             |
|------------------------|----------------------------------------------------------------------|
| **Compute Engine**     | Hosts local MQTT broker (Mosquitto) for simulated telemetry          |
| **Pub/Sub**            | Message buffering and decoupling between MQTT and Dataflow           |
| **Cloud Dataflow**     | Streaming ETL with watermarking, writes raw JSON to GCS              |
| **Cloud Storage (GCS)**| Raw data lake storage (Bronze layer)                                 |
| **Cloud Functions**    | Automatically triggers Spark jobs upon new file arrival in GCS       |
| **Dataproc Serverless**| Spark jobs for validation + transformation (Silver/Gold Delta Lake)  |
| **Delta Lake on GCS**  | ACID-compliant storage with schema evolution, Medallion architecture |
| **Dataproc Metastore** | Centralized schema registry for Delta tables                         |
| **BigQuery**           | BI-ready warehouse layer for analytics and reporting                 |
| **Looker**             | Dashboarding and data visualization                                  |

## 🧪 Medallion Architecture Layers

### 🥉 Bronze Layer (Raw)
- Data is written as-is from Pub/Sub to GCS
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
- Pub/Sub
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

   # Testing 
   mosquitto_sub -h localhost -t "vehicle/telemetry"
   mosquitto_pub -h localhost -t "vehicle/telemetry" -m "TEST DATA"
    ```
2. Simulate MQTT messages from VED dataset:
    ```bash
    python3 ingestion/simulate_telemetry.py --input <FILE_PATH>
    ```
3. Run Pub/Sub ingester:
    ```bash
    export GOOGLE_CLOUD_PROJECT="<PROJECT_ID>"
    python3 ingestion/pubsub_ingestor.py
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