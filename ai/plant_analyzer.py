import os
import json
import base64
from groq import Groq
from google import genai
from google.genai import types

GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

groq_client   = Groq(api_key=GROQ_API_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an expert agricultural AI. Respond ONLY with valid JSON:
{
    "disease_name": "name or Healthy",
    "severity": "None/Mild/Moderate/Severe",
    "severity_score": 0.0,
    "confidence": 0.0,
    "symptoms": ["symptom1"],
    "treatment": {"immediate": ["action1"], "longterm": ["action1"]},
    "prevention": ["tip1"],
    "estimated_yield_loss": 0.0,
    "urgency": "Low/Medium/High/Critical",
    "recommendation": "brief recommendation"
}"""

def analyze_plant_data(crop_type, symptoms, conditions):
    prompt = f"Analyze: Crop={crop_type}, Symptoms={symptoms}, Conditions={conditions}. Return JSON only."
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    text = response.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def analyze_plant_image(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    ext = os.path.splitext(image_path)[1].lower()
    media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
    media_type = media_types.get(ext, "image/jpeg")
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash-lite",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=[
            types.Part.from_bytes(data=image_data, mime_type=media_type),
            "Analyze this plant image for diseases. Return JSON only."
        ]
    )
    text = response.text.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def format_analysis_report(analysis):
    if "error" in analysis:
        return f"Error: {analysis['error']}"
    return f"Disease: {analysis.get('disease_name')}\nSeverity: {analysis.get('severity')}\nRecommendation: {analysis.get('recommendation')}"

if __name__ == "__main__":
    result = analyze_plant_data("Tomato", ["yellow leaves"], {"temperature_c": 30})
    print(result)
