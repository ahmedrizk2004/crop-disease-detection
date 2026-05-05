import os
import json
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an expert agricultural AI assistant specialized in plant disease detection.
Respond ONLY with a valid JSON object in this exact format:
{
    "disease_name": "name of disease or Healthy",
    "severity": "None/Mild/Moderate/Severe",
    "severity_score": 0.0,
    "confidence": 0.0,
    "symptoms": ["symptom1", "symptom2"],
    "treatment": {
        "immediate": ["action1", "action2"],
        "longterm": ["action1", "action2"]
    },
    "prevention": ["tip1", "tip2"],
    "estimated_yield_loss": 0.0,
    "urgency": "Low/Medium/High/Critical",
    "recommendation": "brief overall recommendation"
}"""

def analyze_plant_data(crop_type, symptoms, conditions):
    prompt = f"""Analyze this plant:
Crop: {crop_type}
Symptoms: {', '.join(symptoms)}
Conditions: {json.dumps(conditions)}
Return only JSON."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def analyze_plant_image(image_path):
    import base64
    from pathlib import Path
    path = Path(image_path)
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
    ext = path.suffix.lower()
    media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
    media_type = media_types.get(ext, "image/jpeg")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=[
            types.Part.from_bytes(data=base64.b64decode(image_data), mime_type=media_type),
            "Analyze this plant image. Return only JSON."
        ]
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def format_analysis_report(analysis):
    if "error" in analysis:
        return f"❌ Error: {analysis['error']}"
    return f"""
Disease: {analysis.get('disease_name', 'Unknown')}
Severity: {analysis.get('severity', 'Unknown')}
Confidence: {analysis.get('confidence', 0):.0%}
Urgency: {analysis.get('urgency', 'Unknown')}
Recommendation: {analysis.get('recommendation', 'N/A')}
"""

if __name__ == "__main__":
    result = analyze_plant_data("Tomato", ["yellow leaves", "brown spots"], {"temperature_c": 30})
    print(format_analysis_report(result))
