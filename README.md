<div align="center">

# 🛰️ A.T.L.A.S.

### Anomaly Tracking & Logistics Analytic Segmentation

*ML-gestütztes Supply-Chain-Management-System mit Anomalieerkennung, Lieferanten-Clustering und MLOps-Lifecycle*

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)

</div>

---

## 📋 Über das Projekt

ATLAS ist ein Supply-Chain-Management-System das mithilfe von Machine Learning automatisch **ungewöhnliche Lagerbestände erkennt** und **Lieferanten nach Leistungsprofil gruppiert**. Das System bietet einen vollständigen **MLOps-Lifecycle** mit Model Persistence, Monitoring und Re-Training.

Das System nutzt zwei ML-Modelle:
- **Isolation Forest** — Erkennt Anomalien in Lagerdaten (z.B. unrealistische Mengen oder Preise)
- **K-Means Clustering** — Gruppiert Lieferanten in Premium, Standard und Risiko-Kategorien

## 🖥️ Screenshots

### Dashboard — Übersicht
> Zentrale Kennzahlen auf einen Blick: Produkte, Lieferanten, Kategorien + Datenbank-Erweiterung

### Anomalieerkennung
> Scatter-Plot visualisiert normale Produkte (grün) und erkannte Anomalien (rot)

### Lieferanten-Cluster
> Zwei Scatter-Plots zeigen die Cluster-Trennung über alle 4 Features

### MLOps Monitoring
> Modell-Status, Retrain-Button, Evaluation mit Echtzeit-Metriken

---

## 🏗️ Architektur

```
┌─────────────────┐     HTTP      ┌─────────────────┐     SQL      ┌──────────┐
│    Streamlit     │ ──────────→  │     FastAPI      │ ──────────→  │  SQLite  │
│    Dashboard     │ ←──────────  │   REST API       │ ←──────────  │    DB    │
│    (Port 8501)   │    JSON      │   (Port 8000)    │   Data       │          │
└─────────────────┘               └────────┬─────────┘              └──────────┘
                                           │
                                    ┌──────▼──────┐
                                    │  ML Services │
                                    ├─────────────┤
                                    │ Isolation    │
                                    │ Forest       │
                                    ├─────────────┤
                                    │ K-Means      │
                                    │ Clustering   │
                                    ├─────────────┤
                                    │ Model        │
                                    │ Manager      │
                                    ├─────────────┤
                                    │ Model        │
                                    │ Monitor      │
                                    └──────┬──────┘
                                           │
                                    ┌──────▼──────┐
                                    │  ml_models/  │
                                    │  .joblib     │
                                    │  _meta.json  │
                                    │  monitor_log │
                                    └─────────────┘
```

**Architekturmuster:** MVC (Model-View-Controller)

| Schicht | Technologie | Aufgabe |
|---|---|---|
| **View** | Streamlit + Plotly | Dashboard, Charts, Tabellen |
| **Controller** | FastAPI | REST API, Routing, Validierung |
| **Model** | SQLAlchemy + SQLite | Datenbankzugriff, ORM |
| **Services** | scikit-learn + Pandas | ML-Modelle, Datenverarbeitung |
| **MLOps** | joblib + JSON | Model Persistence, Monitoring |

---

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.11 oder höher
- pip (Python Package Manager)

### Installation

```bash
# Repository klonen
git clone https://github.com/DEIN-USERNAME/ATLAS.git
cd ATLAS

# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren (Windows)
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

### Datenbank befüllen

```bash
py scripts/seed_data.py
```
> Erstellt 500 Produkte, 50 Lieferanten und ~5% bewusste Anomalien

### Starten

```bash
py scripts/start.py
```

| Service | URL |
|---|---|
| Dashboard | http://localhost:8501 |
| API Docs | http://localhost:8000/docs |
| API | http://localhost:8000 |

> Zum Beenden: `Strg + C` im Terminal

---

## 📡 API-Endpunkte

### Inventory
| Methode | Route | Beschreibung |
|---|---|---|
| `GET` | `/api/inventory/` | Alle Produkte abrufen |
| `POST` | `/api/inventory/` | Neues Produkt anlegen |
| `GET` | `/api/inventory/{id}` | Einzelnes Produkt abrufen |
| `POST` | `/api/inventory/seed` | +500 Produkte & +50 Lieferanten hinzufügen |

### Suppliers
| Methode | Route | Beschreibung |
|---|---|---|
| `GET` | `/api/suppliers/` | Alle Lieferanten abrufen |
| `POST` | `/api/suppliers/` | Neuen Lieferanten anlegen |
| `GET` | `/api/suppliers/{id}` | Einzelnen Lieferanten abrufen |

### Machine Learning & MLOps
| Methode | Route | Beschreibung |
|---|---|---|
| `GET` | `/api/ml/anomalies` | Anomalieerkennung ausführen |
| `GET` | `/api/ml/clusters` | Lieferanten-Clustering ausführen |
| `POST` | `/api/ml/retrain` | Modelle löschen und neu trainieren |
| `GET` | `/api/ml/status` | Modell-Status abrufen |
| `POST` | `/api/ml/evaluate` | Modelle evaluieren + ins Log schreiben |

> Interaktive API-Dokumentation: http://localhost:8000/docs

---

## 🤖 ML-Modelle

### Isolation Forest — Anomalieerkennung

| Parameter | Wert |
|---|---|
| Features | `quantity`, `price` |
| Contamination | 5% |
| Methode | Unsupervised Learning |
| Persistenz | `ml_models/isolation_forest.joblib` |

Erkennt Produkte mit ungewöhnlichen Kombinationen aus Menge und Preis.

### K-Means Clustering — Lieferantenbewertung

| Parameter | Wert |
|---|---|
| Features | `delivery_reliability`, `avg_delivery_days`, `price_level`, `quality_score` |
| Cluster | 3 (Premium, Standard, Risiko) |
| Methode | Unsupervised Learning |
| Persistenz | `ml_models/kmeans_clustering.joblib` |

Gruppiert Lieferanten automatisch nach Leistungsprofil.

---

## 🔬 MLOps-Lifecycle

### Model Manager
| Funktion | Aufgabe |
|---|---|
| `save_model()` | Modell + Metadaten speichern (.joblib + _meta.json) |
| `load_model()` | Gespeichertes Modell laden |
| `load_metadata()` | Metadaten laden (Datum, Parameter) |
| `model_exists()` | Prüfen ob Modell vorhanden |

### Model Monitor
| Funktion | Aufgabe |
|---|---|
| `get_model_status()` | Status beider Modelle abrufen |
| `evaluate_models()` | Modelle evaluieren + Ergebnisse ins Log schreiben |

### Lifecycle-Flow
```
Erster Start → Trainieren → Speichern (.joblib)
      ↓
Nächster Aufruf → Laden (schneller!)
      ↓
Neue Daten hinzufügen (+500 via Seed-Button)
      ↓
Evaluate → Performance prüfen
      ↓
Retrain → Neu trainieren mit allen Daten
      ↓
Evaluate → Vorher/Nachher vergleichen
```

---

## 📁 Projektstruktur

```
ATLAS/
├── app/
│   ├── api/
│   │   ├── main.py                  # FastAPI App + Router
│   │   ├── dependencies.py          # Session-Verwaltung
│   │   └── endpoints/
│   │       ├── inventory.py         # CRUD Inventory + Seed
│   │       ├── suppliers.py         # CRUD Suppliers
│   │       └── ml.py               # ML + Retrain + Monitoring
│   ├── models/
│   │   ├── database.py              # DB-Verbindung
│   │   ├── orm_models.py            # Tabellenstruktur
│   │   └── schemas.py              # Pydantic-Schemas
│   ├── services/
│   │   ├── anomaly_detection.py     # Isolation Forest
│   │   ├── clustering.py           # K-Means
│   │   ├── model_manager.py        # Modelle speichern/laden
│   │   └── model_monitor.py        # Monitoring + Evaluation
│   └── frontend/
│       ├── dashboard.py            # Streamlit Dashboard (4 Seiten)
│       └── assets/
│           └── atlas_bg.png        # Hintergrundbild
├── ml_models/                       # Gespeicherte Modelle + Logs
│   ├── isolation_forest.joblib
│   ├── isolation_forest_meta.json
│   ├── kmeans_clustering.joblib
│   ├── kmeans_clustering_meta.json
│   └── monitor_log.json
├── scripts/
│   ├── seed_data.py                # Testdaten-Generator
│   └── start.py                    # Ein-Klick-Start
├── atlas.md                        # Technische Dokumentation
├── requirements.txt                # Dependencies
└── README.md                       # Diese Datei
```

---

## 🗺️ Roadmap

- [x] FastAPI Backend mit CRUD-Endpunkten
- [x] Isolation Forest Anomalieerkennung
- [x] K-Means Lieferanten-Clustering
- [x] Streamlit Dashboard mit Plotly-Charts
- [x] Ein-Klick-Startskript
- [x] Model Manager (speichern/laden mit joblib)
- [x] Model Monitor (Evaluation + Logging)
- [x] MLOps Dashboard-Seite (Status, Retrain, Evaluate)
- [x] Datenbank-Erweiterung per Button (+500 Produkte, +50 Lieferanten)
- [x] Zufällige Anomalie-Rate (2-8%) für realistische Tests
- [ ] Silhouette Score für Cluster-Qualität
- [ ] Elbow Method für optimale Cluster-Anzahl
- [ ] Anomaly Score Statistik + Verteilung
- [ ] Docker Deployment
- [ ] Unit Tests + Integration Tests

---

## 🛠️ Tech Stack

| Paket | Version | Zweck |
|---|---|---|
| FastAPI | 0.128 | REST API Backend |
| SQLAlchemy | 2.0 | ORM + Datenbankzugriff |
| scikit-learn | 1.8 | Machine Learning |
| Pandas | 2.3 | Datenverarbeitung |
| Streamlit | 1.54 | Frontend Dashboard |
| Plotly | 6.5 | Interaktive Charts |
| Pydantic | 2.12 | Datenvalidierung |
| Uvicorn | 0.40 | ASGI Server |
| joblib | (built-in) | Model Persistence |

---

<div align="center">

**Erstellt als ML-Engineering Projekt**

🛰️ *A.T.L.A.S. — Anomaly Tracking & Logistics Analytic Segmentation*

</div>