import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score

PROCESSED_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
MODELS_PATH    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved")

def load_data():
    df = pd.read_csv(os.path.join(PROCESSED_PATH, "crop_data_processed.csv"))
    features = ['temperature_c','humidity_pct','rainfall_mm',
                'nitrogen_ppm','phosphorus_ppm','potassium_ppm',
                'disease_severity','npk_total']
    X = df[features]
    y = df['disease_label']
    return X, y

def train_disease_model():
    print("\n" + "="*50)
    print("🤖 [CNN Simulation] Disease Detection Model")
    print("="*50)

    X, y = load_data()

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    print(f"\n📊 Training samples: {len(X_train)}")
    print(f"📊 Testing  samples: {len(X_test)}")
    print(f"📊 Classes:          {list(le.classes_)}")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )

    print("\n⏳ Training model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)

    print(f"\n✅ Accuracy: {acc*100:.2f}%")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    os.makedirs(MODELS_PATH, exist_ok=True)
    joblib.dump(model,  os.path.join(MODELS_PATH, "disease_model.pkl"))
    joblib.dump(le,     os.path.join(MODELS_PATH, "disease_label_encoder.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_PATH, "disease_scaler.pkl"))
    print(f"\n💾 Model saved to: {MODELS_PATH}/")
    return model, le, scaler

def predict_disease(features: dict):
    model  = joblib.load(os.path.join(MODELS_PATH, "disease_model.pkl"))
    le     = joblib.load(os.path.join(MODELS_PATH, "disease_label_encoder.pkl"))
    scaler = joblib.load(os.path.join(MODELS_PATH, "disease_scaler.pkl"))

    keys = ['temperature_c','humidity_pct','rainfall_mm',
            'nitrogen_ppm','phosphorus_ppm','potassium_ppm',
            'disease_severity','npk_total']
    X = np.array([[features[k] for k in keys]])
    X_scaled = scaler.transform(X)

    pred_idx   = model.predict(X_scaled)[0]
    pred_proba = model.predict_proba(X_scaled)[0]
    disease    = le.inverse_transform([pred_idx])[0]
    confidence = round(float(pred_proba.max()) * 100, 2)

    return {"disease": disease, "confidence": confidence}

if __name__ == "__main__":
    train_disease_model()
