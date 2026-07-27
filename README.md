# CTA Transit Delay Prediction

A geospatial ML pipeline built with XGBoost and scikit-learn on Chicago Transit Authority GTFS data with SQLite persistence. Engineers weather and spatial features to generate 13,800+ delay predictions across 144 CTA rail stops, visualized through an interactive MapLibre GL JS web map.

**[View Live Demo →](https://itbiggs.github.io/Transit_Predictor/)**

## Overview

This project demonstrates end-to-end ML pipeline development for transit prediction:
- **13,824 predictions** across 144 CTA rail stops, 12 months, and 8 time intervals per day
- **Geospatial feature engineering**: distance from Loop, transfer hub detection
- **Weather integration**: Historical Chicago climate data from Visual Crossing API
- **Interactive visualization**: MapLibre GL JS web map with monthly and hourly filtering

## Key Features

### ML Pipeline
- **XGBoost classifier** trained on GTFS data with engineered spatial and weather features
- **SQLite persistence** for efficient data storage and retrieval
- **Feature engineering**: Distance from downtown Loop, transfer hub status, weather conditions
- **Realistic patterns**: Time-of-day multipliers (rush hour peaks) and seasonal variation (winter delays)

### Interactive Web Map
- **MapLibre GL JS** visualization (vanilla JavaScript, no frameworks)
- **144 CTA rail stops** with complete coverage
- **12 monthly predictions** (January-December, using 15th of each month)
- **8 time intervals** per day (12am, 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm)
- **Route geometries** from GTFS shapes.txt for realistic track visualization
- **GeoJSON output** compatible with ArcGIS Online, QGIS, and other mapping tools

> **Note**: This project uses **simulated delays** with realistic spatial propagation patterns to demonstrate ML techniques for transit prediction.

## Technologies

- **Python**: Core pipeline development
- **ML**: XGBoost, scikit-learn, imbalanced-learn
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite
- **Visualization**: Matplotlib, Jupyter Notebook (analysis), MapLibre GL JS (web map)
- **Geospatial**: geopy, GeoJSON, GTFS
- **APIs**: Visual Crossing Weather API

## Setup Instructions

### 1. Clone and setup environment

```bash
git clone https://github.com/ibiggs24/TransitPredictor.git
cd TransitPredictor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Download CTA GTFS data

```bash
curl -L "https://www.transitchicago.com/downloads/sch_data/google_transit.zip" -o /tmp/google_transit.zip
unzip /tmp/google_transit.zip -d data/google_transit/
```

### 3. Set up Visual Crossing API key

Create a `.env` file in the root directory:

```env
VC_API_KEY=your_api_key_here
```

Get a free API key at [Visual Crossing](https://www.visualcrossing.com/weather-api).

### 4. Run the pipeline

```bash
# Load GTFS into SQLite (use sample version for faster testing)
python scripts/load_gtfs_sample.py

# Simulate delays with spatial propagation
python scripts/label_delays.py

# Enrich with weather data
python scripts/join_weather_features.py

# Add spatial features (distance from Loop, transfer hub, etc.)
python scripts/add_spatial_features.py

# Train XGBoost model with spatial features
python scripts/train_xgboost_gridsearch.py

# Generate multi-date GeoJSON predictions with realistic patterns
python scripts/generate_multidate_geojson.py

# Generate route geometries from GTFS shapes
python scripts/generate_routes_geojson.py
```

### 5. View the map

Open `docs/index.html` in your browser or deploy to GitHub Pages:

1. Go to Settings > Pages in your GitHub repo
2. Select "Deploy from a branch"
3. Choose `main` branch and `/docs` folder
4. Visit `https://yourusername.github.io/TransitPredictor/`

## Pipeline Architecture

```
GTFS Data → SQLite Persistence → Delay Simulation → Weather Enrichment → Spatial Feature Engineering → XGBoost Training → GeoJSON Generation → MapLibre Web Map
```

**Engineered Features:**
- `distance_from_loop`: Distance in km from downtown Chicago Loop (41.8781°N, 87.6298°W)
- `is_transfer_hub`: Binary indicator for transfer stations
- Weather features: Temperature, precipitation, wind speed from Visual Crossing API
- Temporal features: Hour of day, day of week, month, season

**Prediction Output:**
- **13,824 total predictions** (144 stops × 8 hours × 12 months)
- Time-based multipliers: Rush hour peaks (9am, 6pm), overnight lows (3am)
- Seasonal patterns: Winter delays (1.4x), summer efficiency (0.85x)

## Project Structure

```
TransitPredictor/
├── scripts/
│   ├── load_gtfs_sample.py            # Load GTFS into SQLite
│   ├── label_delays.py                # Simulate delays with propagation
│   ├── join_weather_features.py       # Enrich with weather data
│   ├── add_spatial_features.py        # Engineer spatial features
│   ├── train_xgboost_gridsearch.py    # Train XGBoost classifier
│   ├── generate_multidate_geojson.py  # Generate 13,824 predictions
│   └── generate_routes_geojson.py     # Extract CTA route geometries
├── notebooks/
│   └── model_training.ipynb           # Jupyter analysis and visualization
├── docs/
│   ├── index.html                     # MapLibre web map (vanilla JS)
│   └── predictions/
│       ├── predictions_multidate.geojson  # 13,824 predictions (144 stops × 8 hours × 12 months)
│       └── routes.geojson                 # CTA route geometries from GTFS shapes
├── data/google_transit/               # GTFS files (gitignored)
├── smart_transit.db                   # SQLite database (gitignored)
├── .env                               # API keys (gitignored)
└── requirements.txt                   # Python dependencies
```

## Author

**Isaac Biggs**
CS + Geography/GIS, Data Science Minor
University of Illinois Urbana-Champaign

Data sources: CTA GTFS Feed, Visual Crossing Weather API
