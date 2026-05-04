import pandas as pd
import os

DATA_PATH = "CropProject/data"

def extract_crop_data():
    path = os.path.join(DATA_PATH, "crop_data.csv")
    df = pd.read_csv(path)
    print(f"✅ Extracted crop_data:        {len(df)} rows")
    return df

def extract_weather_data():
    path = os.path.join(DATA_PATH, "weather_data.csv")
    df = pd.read_csv(path)
    print(f"✅ Extracted weather_data:     {len(df)} rows")
    return df

def extract_disease_images():
    path = os.path.join(DATA_PATH, "disease_images_metadata.csv")
    df = pd.read_csv(path)
    print(f"✅ Extracted disease_images:   {len(df)} rows")
    return df

def extract_yield_predictions():
    path = os.path.join(DATA_PATH, "yield_predictions.csv")
    df = pd.read_csv(path)
    print(f"✅ Extracted yield_predictions:{len(df)} rows")
    return df

def extract_all():
    print("\n📥 [EXTRACT] Reading all CSV files...\n")
    return {
        "crop":    extract_crop_data(),
        "weather": extract_weather_data(),
        "images":  extract_disease_images(),
        "yields":  extract_yield_predictions()
    }
