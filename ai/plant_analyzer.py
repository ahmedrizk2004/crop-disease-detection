import os
import json
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

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
    response = client.chat.completions.create(
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
    prompt = "A plant image was uploaded showing possible disease symptoms. Analyze and detect the most likely plant disease. Return JSON only."
    response = client.chat.completions.create(
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

def format_analysis_report(analysis):
    if "error" in analysis:
        return f"Error: {analysis['error']}"
    return f"Disease: {analysis.get('disease_name')}\nSeverity: {analysis.get('severity')}\nRecommendation: {analysis.get('recommendation')}"

if __name__ == "__main__":
    result = analyze_plant_data("Tomato", ["yellow leaves"], {"temperature_c": 30})
    print(result)
