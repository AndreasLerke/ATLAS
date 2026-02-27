import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from app.models.orm_models import Inventory
from app.services.model_manager import save_model, load_model, model_exists

FEATURE_COLUMNS = ["quantity", "price"]
CONTAMINATION = 0.05
RANDOM_STATE = 42

def get_inventory_dataframe(db: Session) -> pd.DataFrame:
    """Lädt alle Inventory-Daten aus der DB in einen Pandas Dataframe"""
    items = db.query(Inventory).all()

    data = [{
        "id" : item.id,
        "product_name" : item.product_name,
        "quantity" : item.quantity,
        "price" : item.price,
        "category" : item.category 
    } for item in items]

    return pd.DataFrame(data)

def find_optimal_contamination(db:Session):
    """Testet verschiedene Contamination-Werte und findet den Optimlasten."""

    df = get_inventory_dataframe(db)

    if df.empty:
        return {"error": "Keine Daten vorhanden"}

    features = df[FEATURE_COLUMNS]

    # Verschiedene Contamination-Werte testen
    test_values = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    results = []

    for cont in test_values:
        model = IsolationForest(
            contamination = cont,
            random_state = RANDOM_STATE,
            n_estimators = 100
        )
        model.fit(features)

        scores = model.decision_function(features)
        predictions = model.predict(features)
        n_anomalies = int((predictions == -1).sum())

        # Score-Verteilung analysieren
        score_spread = round(float(scores.std()), 4)
        mean_anomaly_score = round(float(scores[predictions == -1].mean()), 4)
        mean_normal_score = round(float(scores[predictions == 1].mean()), 4)

        # Trennung zwischen normal und anomal (je größer desto bessser)
        separation = round(abs(mean_normal_score - mean_anomaly_score), 4)

        results.append({
            "contamination": cont,
            "anomalies_found": n_anomalies,
            "anomaly_percentage": round(n_anomalies / len(df) * 100, 2),
            "score_spread": score_spread,
            "separation": separation,
            "mean_anomaly_score": mean_anomaly_score,
            "mean_normal_score": mean_normal_score
        })

    # Beste Contamination finden (höchste Separation)
    best = max(results, key = lambda x: x["separation"])

    return {
        "results": results,
        "optimal_contamination": best["contamination"],
        "best_separation": best["separation"],
        "aktuelle_contamination": CONTAMINATION
    }

def detect_anomalies(db: Session) -> dict:
    """Führt Isolation Forest auf den Inventory-Daten aus."""

    # === 1. Daten laden ===
    df = get_inventory_dataframe(db)

    if df.empty:
        return {"error": "Keine Daten vorhanden"}
    
    # === 2. Features extrahieren ===
    features = df[FEATURE_COLUMNS]

    # === 3. Modell erstellen oder neu trainieren ===
    model = None

    if model_exists("isolation_forest"):
        model = load_model("isolation_forest")
    
    if model is None:
        model = IsolationForest(
            contamination = CONTAMINATION,
            random_state = RANDOM_STATE,
            n_estimators = 100
        )

        model.fit(features)
        save_model(model, "isolation_forest", {
            "anzahl_datenpunkte": len(df),
            "contamination": CONTAMINATION,
            "features": FEATURE_COLUMNS,
            "mean_score": round(float(model.decision_function(features).mean()), 4)
        })

    # === 4. Vorhersage treffen und Statistiken berechnen ===
    df["anomaly_score"] = model.decision_function(features)
    df["is_anomaly"] = model.predict(features)

    scores = df["anomaly_score"]
    score_stats = {
        "mean": round(float(scores.mean()), 4),
        "std": round(float(scores.std()), 4),
        "min": round(float(scores.min()), 4),
        "max": round(float(scores.max()), 4),
        "median": round(float(scores.median()), 4)
    }

    # === 5. Ergebnisse aufbereiten ===
    anomalies = df[df["is_anomaly"] == -1 ].to_dict(orient = "records")
    normal = df[df["is_anomaly"] == 1 ].to_dict(orient = "records")

    return {
        "total_items": len(df),
        "total_anomalies": len(anomalies),
        "anomaly_percentage": round(len(anomalies) / len(df) * 100, 2),
        "score_stats": score_stats,
        "anomalies": anomalies,
        "normal_items": len(normal),
        "model_params": {
            "contamination": CONTAMINATION,
            "features_used": FEATURE_COLUMNS,
            "n_estimators": 100
        }
    }