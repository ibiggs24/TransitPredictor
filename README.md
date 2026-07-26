# CTA Transit Delay Prediction

A geospatial machine learning pipeline that predicts transit delays for the Chicago Transit Authority (CTA) using GTFS data, weather enrichment, and spatial feature engineering. Interactive web map displays monthly predictions across all CTA rail stops with realistic time-of-day and seasonal patterns.

**[View Live Demo →](https://ibiggs24.github.io/TransitPredictor/)**

## Key Features

### Spatial ML Pipeline
- **Spatial features**: distance from Loop, transfer hub detection
- **Seasonal variation**: Monthly weather patterns (Chicago climate averages)
- **Time-of-day realism**: Hour-based multipliers (rush hour peaks, minimal 3am delays)
- **XGBoost classifier**: Trained on GTFS data with weather enrichment

### Interactive Visualization
- **Vanilla JavaScript** with MapLibre GL JS (no frameworks)
- **All 144 CTA rail stops** with monthly predictions
- **12 months of predictions** (January-December using 15th of each month)
- **8 time intervals** per day (12am, 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm)
- **Route geometries** from GTFS shapes.txt (curved, realistic tracks)
- **GeoJSON format** compatible with ArcGIS Online, QGIS, and other mapping tools

### Realistic Patterns
- **Winter delays**: Higher probability during cold months (January 40% increase)
- **Summer efficiency**: Lower delays in warm months (June 15% decrease)
- **Rush hour peaks**: 9am and 6pm show highest delays
- **Overnight lows**: Minimal delays at 3am (trains run efficiently with low ridership)

> **Note**: This project uses **simulated delays** with realistic spatial propagation, not actual CTA data. The simulation demonstrates ML techniques for transit prediction.

## Technologies

- **ML**: XGBoost, scikit-learn
- **Geospatial**: geopy, GeoJSON
- **Data**: pandas, SQLite, GTFS
- **Visualization**: Vanilla JavaScript, MapLibre GL JS
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
GTFS Data → SQLite → Delay Simulation → Weather Enrichment → Spatial Features → XGBoost → Multi-Date GeoJSON → MapLibre Map
```

**Spatial features:**
- `distance_from_loop`: Distance in km from downtown Chicago (41.8781°N, 87.6298°W)
- `is_transfer_hub`: Binary flag for transfer stations

**Realistic multipliers:**
- **Month-based**: Winter 1.4x delays, Summer 0.85x delays
- **Hour-based**: Rush hour 1.0x, 3am 0.02x (minimal delays)

## Project Structure

```
TransitPredictor/
├── scripts/
│   ├── load_gtfs_sample.py            # Load GTFS into SQLite
│   ├── label_delays.py                # Simulate delays with propagation
│   ├── join_weather_features.py       # Add weather data
│   ├── add_spatial_features.py        # Calculate spatial features
│   ├── train_xgboost_gridsearch.py    # Train XGBoost model
│   ├── generate_multidate_geojson.py  # Create 12-month predictions
│   └── generate_routes_geojson.py     # Extract route geometries
├── docs/
│   ├── index.html                     # MapLibre web map (vanilla JS)
│   └── predictions/
│       ├── predictions_multidate.geojson  # 12 months × 144 stops × 8 hours
│       └── routes.geojson                 # CTA route geometries
├── data/google_transit/               # GTFS files (gitignored)
├── smart_transit.db                   # SQLite database (gitignored)
├── .env                               # API keys (gitignored)
└── requirements.txt
```

## Author

**Isaac Biggs**
CS + Geography/GIS, Data Science Minor
University of Illinois Urbana-Champaign

Data sources: CTA GTFS Feed, Visual Crossing Weather API
