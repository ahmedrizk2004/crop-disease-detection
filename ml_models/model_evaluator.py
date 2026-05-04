import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (accuracy_score, classification_report,
                             mean_absolute_error, r2_score)

PROCESSED_PATH = "CropProject/data/processed"
MODELS_PATH    = "CropProject/ml_models/saved"

def evaluate_disease_model():
    print("\n" + "="*50)
    print("📊 Evaluating Disease Detection Model")
    print("="*50)

    model  = joblib.load(os.path.join(MODELS_PATH, "disease_model.pkl"))
    le     = joblib.load(os.path.join(MODELS_PATH, "disease_label_encoder.pkl"))
    scaler = joblib.load(os.path.join(MODELS_PATH, "disease_scaler.pkl"))

    df = pd.read_csv(os.path.join(PROCESSED_PATH, "crop_data_processed.csv"))
    features = ['temperature_c','humidity_pct','rainfall_mm',
                'nitrogen_ppm','phosphorus_ppm','potassium_ppm',
                'disease_severity','npk_total']
    X = scaler.transform(df[features])
    y = le.transform(df['disease_label'])

    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"\n✅ Cross-Validation Accuracy: {scores.mean()*100:.2f}% (+/- {scores.std()*100:.2f}%)")
    print(f"   Scores per fold: {[f'{s*100:.1f}%' for s in scores]}")

    importances = model.feature_importances_
    print(f"\n📌 Top Features:")
    for name, imp in sorted(zip(features, importances), key=lambda x: -x[1]):
        print(f"   {name:<25} {imp:.4f}")

def evaluate_yield_model():
    print("\n" + "="*50)
    print("📊 Evaluating Yield Prediction Model")
    print("="*50)

    model     = joblib.load(os.path.join(MODELS_PATH, "yield_model.pkl"))
    scaler    = joblib.load(os.path.join(MODELS_PATH, "yield_scaler.pkl"))
    le_crop   = joblib.load(os.path.join(MODELS_PATH, "yield_le_crop.pkl"))
    le_soil   = joblib.load(os.path.join(MODELS_PATH, "yield_le_soil.pkl"))
    le_season = joblib.load(os.path.join(MODELS_PATH, "yield_le_season.pkl"))

    df = pd.read_csv(os.path.join(PROCESSED_PATH, "crop_data_processed.csv"))
    df['crop_encoded']   = le_crop.transform(df['crop_type'])
    df['soil_encoded']   = le_soil.transform(df['soil_type'])
    df['season_encoded'] = le_season.transform(df['season'])

    features = ['crop_encoded','soil_encoded','season_encoded',
                'temperature_c','humidity_pct','rainfall_mm',
                'nitrogen_ppm','phosphorus_ppm','potassium_ppm',
                'disease_severity','npk_total','is_diseased']
    X = scaler.transform(df[features])
    y = df['yield_kg_per_hectare']

    scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print(f"\n✅ Cross-Validation R²: {scores.mean():.4f} (+/- {scores.std():.4f})")
    print(f"   Scores per fold: {[f'{s:.3f}' for s in scores]}")

if __name__ == "__main__":
    evaluate_disease_model()
    evaluate_yield_model()
    print("\n🎉 Evaluation Complete!")
