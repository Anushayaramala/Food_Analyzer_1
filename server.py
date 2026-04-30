# ============================================================
# Flask server — connects the HTML UI to food_analyzer.py
# ============================================================
# How it works:
#   1. Browser sends image URL to this server
#   2. Server calls analyze_food_image() from food_analyzer.py
#   3. Server sends the result back to the browser as JSON
# ============================================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import re
import os

# Import your existing analyzer function directly!
from food_analyzer import analyze_food_image

app = Flask(__name__)
CORS(app)  # Allows the browser to talk to this server

# --- Route 1: Serve the HTML UI ---
# Opens food_analyzer_ui.html when you visit http://localhost:5000
@app.route("/")
def index():
    return send_from_directory(".", "food_analyzer_ui_local.html")


# --- Route 2: Analyze endpoint ---
# The UI calls POST /analyze with {"url": "https://..."}
# This calls your Python function and returns structured JSON
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    image_url = data.get("url", "").strip()

    if not image_url:
        return jsonify({"error": "No URL provided"}), 400

    # Call your existing function from food_analyzer.py
    raw_result = analyze_food_image(image_url)

    # Parse the text output into structured JSON for the UI
    parsed = parse_analysis(raw_result)
    return jsonify(parsed)


def parse_analysis(text: str) -> dict:
    """
    Convert the formatted text from food_analyzer.py into
    a clean JSON object the UI can render directly.
    """

    def extract(pattern, default="—"):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else default

    # Pull out each field with regex
    dish      = extract(r"DISH:\s*(.+)")
    calories  = extract(r"Calories:\s*([\d,]+)")
    protein   = extract(r"Protein:\s*([^\n]+)")
    carbs     = extract(r"Carbs:\s*([^\n]+)")
    fat       = extract(r"Fat:\s*([^\n]+)")
    insight   = extract(r"QUICK INSIGHT:\s*\n\s*(.+?)(?:\n|$)")

    # Health score — grab just the number
    score_raw = extract(r"HEALTH SCORE:\s*([\d.]+)", "5")
    try:
        health_score = int(float(score_raw))
    except:
        health_score = 5

    # Ingredients — grab bullet points from the ingredients section
    ing_section = re.search(
        r"MAIN INGREDIENTS:(.*?)(?:ALLERGENS|HEALTH SCORE)", text, re.DOTALL | re.IGNORECASE
    )
    ingredients = []
    if ing_section:
        ingredients = re.findall(r"•\s*(.+)", ing_section.group(1))
        ingredients = [i.strip() for i in ingredients if i.strip()]

    # Allergens — grab bullet points from allergens section
    alg_section = re.search(
        r"ALLERGENS:(.*?)(?:HEALTH SCORE|💚)", text, re.DOTALL | re.IGNORECASE
    )
    allergens = []
    if alg_section:
        allergens = re.findall(r"•\s*(.+)", alg_section.group(1))
        allergens = [a.strip() for a in allergens if a.strip()]
    if not allergens:
        allergens = ["None detected"]

    # If there was an error in analysis, pass it through
    if text.startswith("❌"):
        return {"error": text}

    return {
        "dish":         dish,
        "calories":     calories.replace(",", ""),
        "protein":      protein,
        "carbs":        carbs,
        "fat":          fat,
        "health_score": health_score,
        "ingredients":  ingredients[:6],
        "allergens":    allergens,
        "insight":      insight
    }


if __name__ == "__main__":
    print("=" * 50)
    print("  AI Food Analyzer — Web UI Server")
    print("=" * 50)
    print("  Open your browser at: http://localhost:5000")
    print("  Press Ctrl+C to stop the server")
    print("=" * 50)
    app.run(debug=True, port=5000)
