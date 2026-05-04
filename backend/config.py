import os
 
class Config:
    SECRET_KEY         = "crop-disease-secret-key-2024"
 
    # AI API Keys
    GEMINI_API_KEY     = "AIzaSyDuQVsh_-4LioVckzfhUEVtLKf2_qDz-S8"
    GROQ_API_KEY       = "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"
 
    # Paths
    MODELS_PATH        = "CropProject/ml_models/saved"
    PROCESSED_PATH     = "CropProject/data/processed"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER      = "CropProject/uploads"
    DEBUG              = True
 