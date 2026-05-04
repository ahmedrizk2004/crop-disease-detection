import pandas as pd
import os

PROCESSED_PATH = "CropProject/data/processed"

def load_all(data: dict):
    print("\n" + "="*50)
    print("💾 [LOAD] Saving processed data...")
    print("="*50)
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    files = {
        "crop_data_processed.csv":           data["crop"],
        "weather_data_processed.csv":        data["weather"],
        "disease_images_processed.csv":      data["images"],
        "yield_predictions_processed.csv":   data["yields"]
    }
    for filename, df in files.items():
        path = os.path.join(PROCESSED_PATH, filename)
        df.to_csv(path, index=False)
        print(f"   ✅ Saved: {filename} ({len(df)} rows)")
    print(f"\n🎉 All processed files saved to: {PROCESSED_PATH}/")
