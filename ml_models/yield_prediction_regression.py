import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROCESSED_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
MODELS_PATH    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved")

def load_data():
    df = pd.read_csv(os.path.join(PROCESSED_PATH, "crop_data_processed.csv"))

    le_crop   = LabelEncoder()
    le_soil   = LabelEncoder()
    le_season = LabelEncoder()

    df['crop_encoded']   = le_crop.fit_transform(df['crop_type'])
    df['soil_encoded']   = le_soil.fit_transform(df['soil_type'])
    df['season_encoded'] = le_season.fit_transform(df['season'])

    features = ['crop_encoded','soil_encoded','season_encoded',
                'temperature_c','humidity_pct','rainfall_mm',
                'nitrogen_ppm','phosphorus_ppm','potassium_ppm',
                'disease_severity','npk_total','is_diseased']
    X = df[features]
    y = df['yield_kg_per_hectare']

    return X, y, le_crop, le_soil, le_season

def train_yield_model():
    print("\n" + "="*50)
    print("📈 [Regression] Yield Prediction Model")
    print("="*50)

    X, y, le_crop, le_soil, le_season = load_data()

    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    print(f"\n📊 Training samples: {len(X_train)}")
    print(f"📊 Testing  samples: {len(X_test)}")

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    print("\n⏳ Training model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae    = mean_absolute_error(y_test, y_pred)
    rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
    r2     = r2_score(y_test, y_pred)

    print(f"\n✅ R² Score: {r2:.4f}")
    print(f"✅ MAE:      {mae:.2f} kg/hectare")
    print(f"✅ RMSE:     {rmse:.2f} kg/hectare")

    os.makedirs(MODELS_PATH, exist_ok=True)
    joblib.dump(model,     os.path.join(MODELS_PATH, "yield_model.pkl"))
    joblib.dump(scaler,    os.path.join(MODELS_PATH, "yield_scaler.pkl"))
    joblib.dump(le_crop,   os.path.join(MODELS_PATH, "yield_le_crop.pkl"))
    joblib.dump(le_soil,   os.path.join(MODELS_PATH, "yield_le_soil.pkl"))
    joblib.dump(le_season, os.path.join(MODELS_PATH, "yield_le_season.pkl"))
    print(f"\n💾 Model saved to: {MODELS_PATH}/")
    return model, scaler

def predict_yield(features: dict):
    model     = joblib.load(os.path.join(MODELS_PATH, "yield_model.pkl"))
    scaler    = joblib.load(os.path.join(MODELS_PATH, "yield_scaler.pkl"))
    le_crop   = joblib.load(os.path.join(MODELS_PATH, "yield_le_crop.pkl"))
    le_soil   = joblib.load(os.path.join(MODELS_PATH, "yield_le_soil.pkl"))
    le_season = joblib.load(os.path.join(MODELS_PATH, "yield_le_season.pkl"))

    crop_enc   = le_crop.transform([features['crop_type']])[0]
    soil_enc   = le_soil.transform([features['soil_type']])[0]
    season_enc = le_season.transform([features['season']])[0]

    X = np.array([[crop_enc, soil_enc, season_enc,
                   features['temperature_c'], features['humidity_pct'],
                   features['rainfall_mm'],   features['nitrogen_ppm'],
                   features['phosphorus_ppm'],features['potassium_ppm'],
                   features['disease_severity'], features['npk_total'],
                   features['is_diseased']]])
    X_scaled = scaler.transform(X)
    predicted = model.predict(X_scaled)[0]
    return {"predicted_yield_kg_per_hectare": round(float(predicted), 2)}

if __name__ == "__main__":
    train_yield_model()
