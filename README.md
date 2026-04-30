# 🤖 AI Food Analyzer — powered by GPT-4o Vision

Paste any food image URL → get instant nutrition analysis, ingredients, allergens, and a health score.

Built with **Python** + **OpenAI GPT-4o Vision API** in under 50 lines of core logic.

---

## 🎯 What it does

- Identifies the dish from any food photo
- Estimates calories, protein, carbs, and fat
- Lists main ingredients
- Flags common allergens (gluten, dairy, nuts, eggs, soy)
- Gives a health score out of 10
- Provides a personalized nutrition tip

## 📸 Sample output

```
🍽️  DISH: Chicken Biryani

📊  NUTRITION ESTIMATE (per serving):
   • Calories: 520 kcal
   • Protein: 32g
   • Carbs: 58g
   • Fat: 14g

🥗  MAIN INGREDIENTS:
   • Basmati rice
   • Chicken
   • Yogurt marinade
   • Saffron
   • Whole spices (cardamom, cloves, bay leaf)

⚠️  ALLERGENS:
   • Dairy (yogurt)

💚  HEALTH SCORE: 7/10
   A well-balanced meal with good protein content and aromatic spices.

📝  QUICK INSIGHT:
   Biryani is a satisfying, nutrient-rich dish. To make it lighter,
   reduce the ghee and add more vegetables like peas or carrots.
```

---

## 🚀 Setup (3 steps)

**1. Install the OpenAI library**
```bash
pip install openai
```

**2. Get your API key**
Sign up at [platform.openai.com](https://platform.openai.com/api-keys) → Create new secret key

**3. Add your key + run**
```bash
# Option A: environment variable (recommended)
export OPENAI_API_KEY="your-key-here"
python food_analyzer.py

# Option B: paste directly in food_analyzer.py line 16
```

---

## 💡 How it works

```
Your image URL
      ↓
GPT-4o Vision API  ←  System prompt (nutrition expert persona)
      ↓
Structured analysis (calories, ingredients, allergens, health score)
```

The core insight: GPT-4o already knows nutrition science. The system prompt just tells it *how* to format and present that knowledge.

---

## 🛠️ Tech stack

- Python 3.8+
- OpenAI Python SDK (`openai`)
- GPT-4o Vision (multimodal LLM)

---

## 📬 Connect

Built by [Your Name] · [Your LinkedIn URL]  
Part of my #BuildingInPublic AI engineering journey.

---
*Cost to run: ~$0.01–0.03 per image analysis*
