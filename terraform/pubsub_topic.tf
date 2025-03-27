resource "google_pubsub_topic" "vehicle_telemetry_raw" {
  name                       = "vehicle-telemetry-raw"
  message_retention_duration = "604800s"  # 7 days
  labels                     = {
    environment = "dev"
    source      = "vehicle-ingestion"
  }
}