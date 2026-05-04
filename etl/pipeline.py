import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract   import extract_all
from etl.transform import transform_all
from etl.load      import load_all

def run_pipeline():
    print("\n" + "="*50)
    print("🚀 ETL PIPELINE - Crop Disease Detection System")
    print("="*50)
    raw_data       = extract_all()
    processed_data = transform_all(raw_data)
    load_all(processed_data)
    print("\n" + "="*50)
    print("✅ ETL Pipeline completed successfully!")
    print("="*50)
    return processed_data

if __name__ == "__main__":
    run_pipeline()
