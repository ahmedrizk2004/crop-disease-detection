import pandas as pd

def transform_crop_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n🔄 [TRANSFORM] crop_data...")
    before = len(df)
    df = df.drop_duplicates()
    print(f"   Duplicates removed:     {before - len(df)}")
    df['temperature_c'].fillna(df['temperature_c'].mean(), inplace=True)
    df['humidity_pct'].fillna(df['humidity_pct'].mean(), inplace=True)
    df['rainfall_mm'].fillna(0, inplace=True)
    df['disease_severity'].fillna(0, inplace=True)
    df = df[df['temperature_c'].between(-10, 55)]
    df = df[df['humidity_pct'].between(0, 100)]
    df = df[df['yield_kg_per_hectare'] > 0]
    df['crop_type']     = df['crop_type'].str.strip().str.title()
    df['disease_label'] = df['disease_label'].str.strip().str.title()
    df['soil_type']     = df['soil_type'].str.strip().str.title()
    df['season']        = df['season'].str.strip().str.title()
    df['is_diseased']   = (df['disease_label'] != 'Healthy').astype(int)
    df['npk_total']     = df['nitrogen_ppm'] + df['phosphorus_ppm'] + df['potassium_ppm']
    df['yield_category'] = pd.cut(
        df['yield_kg_per_hectare'],
        bins=[0, 3000, 8000, 20000, 999999],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    print(f"   Final rows:             {len(df)}")
    print(f"   Diseased crops:         {df['is_diseased'].sum()}")
    return df

def transform_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n🔄 [TRANSFORM] weather_data...")
    df = df.drop_duplicates()
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day_of_year'] = df['date'].dt.dayofyear
    df = df[df['temperature_c'].between(-20, 60)]
    df = df[df['humidity_pct'].between(0, 100)]
    df['rainfall_mm'] = df['rainfall_mm'].clip(lower=0)
    df['heat_index'] = df['temperature_c'] * 0.6 + df['humidity_pct'] * 0.4
    df['season'] = df['month'].map({
        12:'Winter', 1:'Winter', 2:'Winter',
        3:'Spring',  4:'Spring', 5:'Spring',
        6:'Summer',  7:'Summer', 8:'Summer',
        9:'Autumn', 10:'Autumn', 11:'Autumn'
    })
    print(f"   Final rows:             {len(df)}")
    return df

def transform_disease_images(df: pd.DataFrame) -> pd.DataFrame:
    print("\n🔄 [TRANSFORM] disease_images_metadata...")
    df = df.drop_duplicates()
    df['crop_type']     = df['crop_type'].str.strip().str.title()
    df['disease_label'] = df['disease_label'].str.strip().str.title()
    df = df[df['confidence_score'] >= 0.75]
    df['is_annotated'] = df['annotated'].astype(bool)
    print(f"   Final rows (quality >= 0.75): {len(df)}")
    return df

def transform_yield_predictions(df: pd.DataFrame) -> pd.DataFrame:
    print("\n🔄 [TRANSFORM] yield_predictions...")
    df = df.drop_duplicates()
    df['prediction_date'] = pd.to_datetime(df['prediction_date'])
    df['crop_type']       = df['crop_type'].str.strip().str.title()
    df['accuracy_pct']    = (100 - df['error_pct']).clip(lower=0)
    df['good_prediction'] = (df['error_pct'] < 10).astype(int)
    print(f"   Final rows:             {len(df)}")
    print(f"   Good predictions (<10% error): {df['good_prediction'].sum()}")
    return df

def transform_all(data: dict) -> dict:
    print("\n" + "="*50)
    print("🔄 [TRANSFORM] Starting transformations...")
    print("="*50)
    return {
        "crop":    transform_crop_data(data["crop"]),
        "weather": transform_weather_data(data["weather"]),
        "images":  transform_disease_images(data["images"]),
        "yields":  transform_yield_predictions(data["yields"])
    }
