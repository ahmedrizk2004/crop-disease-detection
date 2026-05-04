from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

# ══════════════════════════════════════════
#  Crop Record
# ══════════════════════════════════════════
@dataclass
class CropRecord:
    crop_id:              int
    crop_type:            str
    soil_type:            str
    season:               str
    temperature_c:        float
    humidity_pct:         float
    rainfall_mm:          float
    nitrogen_ppm:         float
    phosphorus_ppm:       float
    potassium_ppm:        float
    disease_label:        str
    disease_severity:     float
    yield_kg_per_hectare: float
    npk_total:            float        = 0.0
    is_diseased:          int          = 0
    created_at:           str          = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "crop_id":              self.crop_id,
            "crop_type":            self.crop_type,
            "soil_type":            self.soil_type,
            "season":               self.season,
            "temperature_c":        self.temperature_c,
            "humidity_pct":         self.humidity_pct,
            "rainfall_mm":          self.rainfall_mm,
            "nitrogen_ppm":         self.nitrogen_ppm,
            "phosphorus_ppm":       self.phosphorus_ppm,
            "potassium_ppm":        self.potassium_ppm,
            "disease_label":        self.disease_label,
            "disease_severity":     self.disease_severity,
            "yield_kg_per_hectare": self.yield_kg_per_hectare,
            "npk_total":            self.npk_total,
            "is_diseased":          self.is_diseased,
            "created_at":           self.created_at,
        }


# ══════════════════════════════════════════
#  Disease Prediction Result
# ══════════════════════════════════════════
@dataclass
class DiseasePrediction:
    prediction_id:  int
    crop_type:      str
    disease:        str
    confidence:     float
    input_features: dict
    created_at:     str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "prediction_id":  self.prediction_id,
            "crop_type":      self.crop_type,
            "disease":        self.disease,
            "confidence":     self.confidence,
            "input_features": self.input_features,
            "created_at":     self.created_at,
        }


# ══════════════════════════════════════════
#  Yield Prediction Result
# ══════════════════════════════════════════
@dataclass
class YieldPrediction:
    prediction_id:            int
    crop_type:                str
    predicted_yield:          float
    actual_yield:             Optional[float]
    input_features:           dict
    created_at:               str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "prediction_id":   self.prediction_id,
            "crop_type":       self.crop_type,
            "predicted_yield": self.predicted_yield,
            "actual_yield":    self.actual_yield,
            "input_features":  self.input_features,
            "created_at":      self.created_at,
        }


# ══════════════════════════════════════════
#  AI Plant Analysis Result
# ══════════════════════════════════════════
@dataclass
class PlantAnalysis:
    analysis_id:         int
    crop_type:           str
    disease_name:        str
    severity:            str
    severity_score:      float
    confidence:          float
    urgency:             str
    estimated_yield_loss: float
    symptoms:            List[str]
    treatment_immediate: List[str]
    treatment_longterm:  List[str]
    prevention:          List[str]
    recommendation:      str
    analysis_type:       str   = "data"   # "data" or "image"
    created_at:          str   = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "analysis_id":          self.analysis_id,
            "crop_type":            self.crop_type,
            "disease_name":         self.disease_name,
            "severity":             self.severity,
            "severity_score":       self.severity_score,
            "confidence":           self.confidence,
            "urgency":              self.urgency,
            "estimated_yield_loss": self.estimated_yield_loss,
            "symptoms":             self.symptoms,
            "treatment_immediate":  self.treatment_immediate,
            "treatment_longterm":   self.treatment_longterm,
            "prevention":           self.prevention,
            "recommendation":       self.recommendation,
            "analysis_type":        self.analysis_type,
            "created_at":           self.created_at,
        }


# ══════════════════════════════════════════
#  Weather Record
# ══════════════════════════════════════════
@dataclass
class WeatherRecord:
    record_id:     int
    region:        str
    date:          str
    temperature_c: float
    humidity_pct:  float
    rainfall_mm:   float
    wind_speed:    float
    frost_risk:    int
    season:        str
    heat_index:    float = 0.0

    def to_dict(self):
        return {
            "record_id":     self.record_id,
            "region":        self.region,
            "date":          self.date,
            "temperature_c": self.temperature_c,
            "humidity_pct":  self.humidity_pct,
            "rainfall_mm":   self.rainfall_mm,
            "wind_speed":    self.wind_speed,
            "frost_risk":    self.frost_risk,
            "season":        self.season,
            "heat_index":    self.heat_index,
        }


# ══════════════════════════════════════════
#  API Response Helpers
# ══════════════════════════════════════════
def success_response(data, message: str = "Success"):
    return {"success": True, "message": message, "data": data}

def error_response(message: str, code: int = 400):
    return {"success": False, "message": message, "error_code": code}
