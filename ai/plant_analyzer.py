import base64
import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import Config

from groq import Groq
groq_client = Groq(api_key=Config.GROQ_API_KEY)

SYSTEM_PROMPT = """You are an expert agricultural AI assistant specialized in plant disease detection and crop health analysis.

When analyzing a plant image or receiving plant data, you must respond ONLY with a valid JSON object in this exact format:
{
    "disease_name": "name of disease or Healthy",
    "severity": "None/Mild/Moderate/Severe",
    "severity_score": 0.0,
    "confidence": 0.0,
    "symptoms": ["symptom1", "symptom2"],
    "treatment": {
        "immediate": ["action1", "action2"],
        "longterm":  ["action1", "action2"]
    },
    "prevention": ["tip1", "tip2"],
    "estimated_yield_loss": 0.0,
    "urgency": "Low/Medium/High/Critical",
    "recommendation": "brief overall recommendation"
}

severity_score is from 0.0 to 1.0
confidence is from 0.0 to 1.0
estimated_yield_loss is percentage from 0 to 100
Return ONLY the JSON object, no extra text."""


def _parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def analyze_plant_image(image_path: str) -> dict:
    path = Path(image_path)
    if not path.exists():
        return {"error": f"Image not found: {image_path}"}
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        ext = path.suffix.lower()
        media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                       ".png": "image/png", ".webp": "image/webp"}
        mime = media_types.get(ext, "image/jpeg")

        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Analyze this plant image for diseases. Return only the JSON response."
                        }
                    ]
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return _parse_json(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Image analysis error: {str(e)}"}


def analyze_plant_data(crop_type: str, symptoms: list, conditions: dict) -> dict:
    prompt = f"""Analyze this plant data and detect diseases:

Crop Type: {crop_type}
Reported Symptoms: {', '.join(symptoms)}
Growing Conditions:
- Temperature:  {conditions.get('temperature_c',  'N/A')}°C
- Humidity:     {conditions.get('humidity_pct',   'N/A')}%
- Rainfall:     {conditions.get('rainfall_mm',    'N/A')} mm
- Soil Type:    {conditions.get('soil_type',      'N/A')}
- Nitrogen:     {conditions.get('nitrogen_ppm',   'N/A')} ppm
- Phosphorus:   {conditions.get('phosphorus_ppm', 'N/A')} ppm
- Potassium:    {conditions.get('potassium_ppm',  'N/A')} ppm

Return only the JSON response."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return _parse_json(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Groq error: {str(e)}"}


def format_analysis_report(analysis: dict) -> str:
    if "error" in analysis:
        return f"❌ Error: {analysis['error']}"

    report = f"""
╔══════════════════════════════════════════╗
║         🌿 PLANT ANALYSIS REPORT         ║
╚══════════════════════════════════════════╝

🦠 Disease:        {analysis.get('disease_name', 'Unknown')}
⚠️  Severity:       {analysis.get('severity', 'Unknown')} (Score: {analysis.get('severity_score', 0):.1%})
🎯 Confidence:     {analysis.get('confidence', 0):.1%}
🚨 Urgency:        {analysis.get('urgency', 'Unknown')}
📉 Yield Loss Est: {analysis.get('estimated_yield_loss', 0):.1f}%

📋 Symptoms:
{chr(10).join(f'   • {s}' for s in analysis.get('symptoms', []))}

💊 Immediate Treatment:
{chr(10).join(f'   • {t}' for t in analysis.get('treatment', {}).get('immediate', []))}

🔬 Long-term Treatment:
{chr(10).join(f'   • {t}' for t in analysis.get('treatment', {}).get('longterm', []))}

🛡️  Prevention Tips:
{chr(10).join(f'   • {p}' for p in analysis.get('prevention', []))}

💡 Recommendation:
   {analysis.get('recommendation', 'N/A')}
"""
    return report


if __name__ == "__main__":
    print("🌿 Testing Plant Analyzer...\n")
    sample = analyze_plant_data(
        crop_type="Tomato",
        symptoms=["yellow leaves", "brown spots", "wilting"],
        conditions={
            "temperature_c":  32,
            "humidity_pct":   80,
            "rainfall_mm":    15,
            "soil_type":      "Loamy",
            "nitrogen_ppm":   45,
            "phosphorus_ppm": 20,
            "potassium_ppm":  100
        }
    )
    print(format_analysis_report(sample))
