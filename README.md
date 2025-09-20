🏎️ Formula 1 Race Prediction Model

This project applies machine learning and sports analytics to predict Formula 1 race outcomes — including podium finishers — using real-time qualifying results and historical race data.

It demonstrates data engineering, feature engineering, and predictive modeling in a real-world sports analytics context.

🚀 Features

Collects 7+ years of race and qualifying data via the FastF1 API
.

Builds an enriched dataset with:

Driver form (last 3 races)

Team performance trends

Circuit-specific driver history

Track characteristics (length, corners, overtaking difficulty, etc.)

Trains a machine learning model (f1_position_model.pkl) to predict finishing positions.

Automatically updates the dataset with latest race results.

Provides a simple interface to predict podiums for upcoming Grands Prix.

📊 Model Performance

Mean Absolute Error (MAE): ~3.4 finishing positions

Exact Podium Accuracy: ~3%

At-least-one-driver-on-podium accuracy: ~40%

⚙️ Example Usage
from podium_model import predict_race_podium

# Predict 2025 Baku GP podium
predicted_podium = predict_race_podium(2025, 17, "Baku")

# Output:
# Predicted Podium:
# 1: NOR
# 2: VER
# 3: PIA

🔮 Future Improvements

Retrain dynamically as new race results are added.

Add features for tyre strategy, pit stops, and weather.

Wrap into a FastAPI REST API for live predictions.

Create an interactive dashboard for visualization.

🛠️ Skills Demonstrated

Data Engineering: Data collection, cleaning, merging with Pandas.

Feature Engineering: Domain-informed metrics (driver/team form, circuit history).

Machine Learning: XGBoost regression, evaluation, and model persistence (joblib).

Pipeline Automation: Auto-updating datasets with latest race results.
