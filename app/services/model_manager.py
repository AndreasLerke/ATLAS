import joblib
import os
import json
from datetime import datetime

# === 1.Pfad zum Modell-Ordner ===
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml_models")

