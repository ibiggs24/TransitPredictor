# Transit Predictor 2025

A Python-based machine learning pipeline to predict delays in the Chicago Transit Authority (CTA) system. This tool processes GTFS data, enriches it with weather, and trains a model to detect potential delays.

## Features

- Parses GTFS stop times and loads into SQLite
- Labels stop delays using schedule deviations
- Enriches transit data with hourly weather from the Visual Crossing API
- Balances imbalanced delay classes using SMOTE
- Trains and saves an XGBoost model with GridSearchCV
- Outputs model evaluation: confusion matrix, precision, recall, F1-score

## Technologies Used

- **Machine Learning**: XGBoost, scikit-learn, SMOTE (imblearn)
- **Data Wrangling**: pandas, SQLite
- **APIs**: Visual Crossing Weather API
- **Dev Tools**: Python-dotenv, joblib, Jupyter Notebook

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ibiggs24/TransitPredictor.git
cd TransitPredictor
```

### 2. Set up Python virtual environment

```bash
python3 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
```

### 3. Set your API key in a `.env` file

Create a `.env` file in the root directory with:

```env
VISUAL_CROSSING_API_KEY=your_api_key_here
```

### 4. Prepare the dataset

Run the following scripts to build and enrich the transit dataset:

```bash
python scripts/load_gtfs.py
python scripts/label_delays.py
python scripts/join_weather_features.py
```

### 5. Train the model

Run XGBoost model training with grid search and SMOTE balancing:

```bash
python scripts/train_xgboost_gridsearch.py
```

This will print evaluation metrics and save the model as `xgb_model.pkl`.

## Notes

* Weather enrichment matches timestamps and location to historical hourly weather
* SMOTE balances classes before model training to improve delay detection
* The model can be reused in a prediction pipeline or web service

## Author

Isaac Biggs

CS + GGIS Major, University of Illinois Urbana-Champaign

Data sources: CTA GTFS Feed, Visual Crossing Weather
