import json
import os
from datetime import datetime

from sqlalchemy.orm import Session

from app.services.anomaly_detection import detect_anomalies
from app.services.clustering import cluster_suppliers
from app.services.model_manager import load_metadata

# === 1. Pfad zur Monitoring-Log Datei ===
MONITOR_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml_models")
MONITOR_LOG = os.path.join(MONITOR_DIR, "monitor_log.json")

