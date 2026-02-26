# 🛰️ A.T.L.A.S.
## Anomaly Tracking & Logistics Analytic Segmentation

### Projektbeschreibung
Supply-Chain-Management-System mit ML-gestützter Anomalieerkennung
und Lieferanten-Clustering. Das System erkennt automatisch ungewöhnliche
Lagerbestände (Isolation Forest) und gruppiert Lieferanten nach
Leistungsprofil (K-Means Clustering). Inklusive MLOps-Lifecycle mit
Model Manager, Model Monitoring und Re-Training.

### Technologie-Stack
| Kategorie | Technologie |
|---|---|
| **Backend** | FastAPI + SQLAlchemy + SQLite |
| **ML** | scikit-learn (Isolation Forest, K-Means) |
| **MLOps** | joblib (Model Persistence) + JSON (Monitoring Logs) |
| **Frontend** | Streamlit + Plotly |
| **Architektur** | MVC Pattern |
| **Sprache** | Python 3.11+ |

### Architektur (MVC)
```
View (Streamlit)  →  Controller (FastAPI)  →  Model/Service (DB + ML)
  dashboard.py        endpoints/*.py           orm_models.py
  Nur anzeigen        Vermittelt               anomaly_detection.py
  Port 8501           Port 8000                clustering.py
                                               model_manager.py
                                               model_monitor.py
```

### Projektstruktur
```
ATLAS/
├── app/
│   ├── api/
│   │   ├── main.py                  FastAPI App + Router
│   │   ├── dependencies.py          Session-Verwaltung (DI)
│   │   └── endpoints/
│   │       ├── inventory.py         Inventory CRUD + Seed Endpunkt
│   │       ├── suppliers.py         Supplier CRUD Endpunkte
│   │       └── ml.py               ML + Retrain + Monitoring Endpunkte
│   ├── models/
│   │   ├── database.py              SQLite + SQLAlchemy Engine
│   │   ├── orm_models.py            Inventory + Supplier Tabellen
│   │   └── schemas.py              Pydantic Validierung
│   ├── services/
│   │   ├── anomaly_detection.py     Isolation Forest Service
│   │   ├── clustering.py           K-Means Clustering Service
│   │   ├── model_manager.py        Modelle speichern/laden (joblib)
│   │   └── model_monitor.py        Modell-Monitoring + Evaluation
│   └── frontend/
│       ├── dashboard.py            Streamlit Dashboard (4 Seiten)
│       └── assets/
│           └── atlas_bg.png        Hintergrundbild
├── ml_models/                       Gespeicherte ML-Modelle + Logs
│   ├── isolation_forest.joblib      Trainiertes Anomalie-Modell
│   ├── isolation_forest_meta.json   Metadaten (Datum, Parameter)
│   ├── kmeans_clustering.joblib     Trainiertes Cluster-Modell
│   ├── kmeans_clustering_meta.json  Metadaten (Datum, Parameter)
│   └── monitor_log.json            Monitoring-Historie
├── scripts/
│   ├── seed_data.py                Testdaten-Generator (erweiterbar)
│   └── start.py                    Ein-Klick-Startskript
├── atlas.md                        Projektdokumentation
├── README.md                       Projekt-Übersicht
└── requirements.txt                Python-Dependencies
```

### API-Endpunkte
| Methode | Route | Beschreibung |
|---|---|---|
| GET | `/api/inventory/` | Alle Produkte abrufen |
| POST | `/api/inventory/` | Neues Produkt anlegen |
| GET | `/api/inventory/{id}` | Einzelnes Produkt abrufen |
| POST | `/api/inventory/seed` | +500 Produkte & +50 Lieferanten hinzufügen |
| GET | `/api/suppliers/` | Alle Lieferanten abrufen |
| POST | `/api/suppliers/` | Neuen Lieferanten anlegen |
| GET | `/api/suppliers/{id}` | Einzelnen Lieferanten abrufen |
| GET | `/api/ml/anomalies` | Isolation Forest ausführen |
| GET | `/api/ml/clusters` | K-Means Clustering ausführen |
| POST | `/api/ml/retrain` | Modelle löschen und neu trainieren |
| GET | `/api/ml/status` | Modell-Status abrufen |
| POST | `/api/ml/evaluate` | Modelle evaluieren + ins Log schreiben |

### ML-Modelle

#### Isolation Forest (Anomalieerkennung)
- **Zweck:** Erkennt ungewöhnliche Lagerbestände
- **Features:** `quantity`, `price`
- **Methode:** Unsupervised Learning — findet Ausreißer ohne Labels
- **Konfiguration:** contamination=0.05, random_state=42
- **Persistenz:** Gespeichert als `isolation_forest.joblib`
- **Ergebnis:** ~5% der Produkte als Anomalien markiert

#### K-Means Clustering (Lieferantenbewertung)
- **Zweck:** Gruppiert Lieferanten nach Leistungsprofil
- **Features:** `delivery_reliability`, `avg_delivery_days`, `price_level`, `quality_score`
- **Methode:** Unsupervised Learning — findet natürliche Gruppen
- **Konfiguration:** n_clusters=3, n_init=10, random_state=42
- **Persistenz:** Gespeichert als `kmeans_clustering.joblib`
- **Ergebnis:** 3 Cluster (Premium, Standard, Risiko)

### MLOps-Lifecycle

#### Model Manager (`model_manager.py`)
| Funktion | Aufgabe |
|---|---|
| `save_model()` | Modell + Metadaten auf Festplatte speichern |
| `load_model()` | Gespeichertes Modell laden |
| `load_metadata()` | Metadaten laden (Datum, Parameter, Score) |
| `model_exists()` | Prüfen ob Modell vorhanden |

#### Model Monitor (`model_monitor.py`)
| Funktion | Aufgabe |
|---|---|
| `get_model_status()` | Status beider Modelle abrufen |
| `evaluate_models()` | Modelle ausführen + Ergebnisse loggen |

#### Lifecycle-Flow
```
1. Erster Start → Modelle trainieren → speichern (.joblib)
2. Nächster Aufruf → gespeichertes Modell laden (schneller!)
3. Neue Daten hinzufügen (+500 Produkte via Seed-Button)
4. Evaluate → Modell-Performance prüfen
5. Retrain → Modelle löschen und mit allen Daten neu trainieren
6. Evaluate → Vergleich vorher/nachher
```

### Testdaten
- **500 Produkte** in 5 Kategorien (Befestigung, Elektronik, Werkzeug, Hydraulik, Verpackung)
- **50 Lieferanten** mit realistischen Leistungsdaten
- **Zufällige Anomalie-Rate** (2-8%) bei jedem Seed-Klick
- **Erweiterbar:** +500 Produkte & +50 Lieferanten per Dashboard-Button

### Dashboard-Seiten
| Seite | Inhalt |
|---|---|
| **Dashboard** | Übersicht: Anzahl Produkte, Lieferanten, Kategorien + Seed-Button |
| **Anomalieerkennung** | Scatter-Plot (Quantity vs. Price), Anomalie-Tabelle |
| **Lieferanten-Cluster** | Cluster-Expander mit Statistiken, zwei Scatter-Plots |
| **MLOps Monitoring** | Modell-Status, Retrain-Button, Evaluate-Button |

### Schnellstart
```bash
# 1. Repository klonen und venv erstellen
cd ATLAS
python -m venv venv
venv\Scripts\activate

# 2. Dependencies installieren
pip install -r requirements.txt

# 3. Datenbank befüllen
py scripts/seed_data.py

# 4. Alles starten
py scripts/start.py

# 5. Im Browser öffnen
# Dashboard: http://localhost:8501
# API Docs:  http://localhost:8000/docs
```

### Geplante Features (Phase 3)
- [ ] **Erweiterte ML-Metriken**
  - Silhouette Score für Cluster-Qualität
  - Elbow Method für optimale Cluster-Anzahl
  - Anomaly Score Verteilung + Statistik
- [ ] **Docker Deployment**
  - Dockerfile + docker-compose.yml
  - SQLite → PostgreSQL Migration
  - Umgebungsvariablen für Konfiguration
- [ ] **Erweiterte ML-Features**
  - Feature Engineering (z.B. Kapitalbindung = quantity × price)
  - Business Rules + ML kombiniert
  - Automatische Cluster-Benennung
- [ ] **Testing**
  - Unit Tests für Services
  - Integration Tests für API-Endpunkte
  - ML-Model Validierung