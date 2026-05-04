import os

class Config:
    SECRET_KEY         = os.environ.get("SECRET_KEY", "crop-disease-secret-key-2024")
    ANTHROPIC_API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY     = os.environ.get("GEMINI_API_KEY", "")
    GROQ_API_KEY       = os.environ.get("GROQ_API_KEY", "")
    MODELS_PATH        = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml_models", "saved")
    PROCESSED_PATH     = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER      = "uploads"
    DEBUG              = False
