# ============================================================
# AI Food Analyzer — powered by GPT-4o Vision
# Built with Python + OpenAI API
# ============================================================
# What this does:
#   Drop in any food image URL → get calories, ingredients,
#   allergens, and a health score back instantly.
# ============================================================

import openai
import os
import requests
import base64
from urllib.parse import urlparse

# --- Setup ---
# Get your API key from: https://platform.openai.com/api-keys
# Option 1: Set it as an environment variable (recommended)
# Option 2: Paste it directly in the quotes below (not for sharing!)
API_KEY = os.getenv("OPENAI_API_KEY", "API_KEY_HERE")

client = openai.OpenAI(api_key=API_KEY)

# --- System Prompt ---
# This is where the magic is. We're telling GPT-4o exactly
# how to behave — like a specialized nutrition expert.
SYSTEM_PROMPT = """
You are an expert nutritionist and food scientist with 20 years of experience.

When given a food image, you ALWAYS respond in this exact format:

🍽️  DISH: [name of the dish]

📊  NUTRITION ESTIMATE (per serving):
   • Calories: [number] kcal
   • Protein: [number]g
   • Carbs: [number]g
   • Fat: [number]g

🥗  MAIN INGREDIENTS:
   • [ingredient 1]
   • [ingredient 2]
   • [ingredient 3]
   (list up to 6)

⚠️  ALLERGENS:
   • [allergen 1] — e.g. Gluten, Dairy, Nuts, Eggs, Soy
   • Write "None detected" if no common allergens present

💚  HEALTH SCORE: [X/10]
   [One sentence explaining the score]

📝  QUICK INSIGHT:
   [2-3 sentences: is this a good meal choice? any tips to make it healthier?]

If the image is NOT food, politely say so and ask for a food image.
Always be encouraging and non-judgmental about food choices.
"""


def url_to_base64(image_url: str):
    """
    Download an image from a URL and convert it to base64.
    This avoids format errors caused by redirect URLs or CDN quirks.
    Returns (base64_string, media_type) or raises an exception.
    """
    headers = {"User-Agent": "Mozilla/5.0"}  # some servers block non-browser requests
    response = requests.get(image_url, headers=headers, timeout=10)
    response.raise_for_status()

    # Detect media type from response headers or URL extension
    content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    
    # Map content types to valid OpenAI formats
    type_map = {
        "image/jpeg": "image/jpeg",
        "image/jpg":  "image/jpeg",
        "image/png":  "image/png",
        "image/gif":  "image/gif",
        "image/webp": "image/webp",
    }

    # Fall back to guessing from URL if header is missing/wrong
    if content_type not in type_map:
        ext = urlparse(image_url).path.lower().split(".")[-1]
        ext_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                   "png": "image/png", "gif": "image/gif", "webp": "image/webp"}
        content_type = ext_map.get(ext, "image/jpeg")

    media_type = type_map.get(content_type, "image/jpeg")
    b64 = base64.standard_b64encode(response.content).decode("utf-8")
    return b64, media_type


def analyze_food_image(image_url: str) -> str:
    """
    Send a food image to GPT-4o Vision and get a full nutrition analysis.
    Downloads the image first and sends it as base64 — works with any URL.

    Args:
        image_url: Any publicly accessible URL to a food image

    Returns:
        A formatted string with the full nutrition analysis
    """
    print("\n🔍 Downloading image...")

    try:
        b64_image, media_type = url_to_base64(image_url)
    except requests.exceptions.HTTPError as e:
        return f"❌ Could not download image (HTTP {e.response.status_code}). Try a different URL."
    except Exception as e:
        return f"❌ Could not download image: {str(e)}"

    print("✅ Image ready! Asking GPT-4o to analyze it...\n")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1000,
            messages=[
                # System message sets the behavior
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                # User message: text + base64 image (works with ANY url)
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this food image for me."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{b64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "❌ Invalid API key. Get yours at: https://platform.openai.com/api-keys"
    except openai.RateLimitError:
        return "❌ Rate limit hit. Wait a moment and try again."
    except Exception as e:
        return f"❌ Something went wrong: {str(e)}"


def main():
    """
    Main loop — keeps asking for images until the user quits.
    """
    print("=" * 55)
    print("   🤖 AI Food Analyzer — powered by GPT-4o Vision")
    print("=" * 55)
    print("Paste any food image URL and I'll analyze it for you.")
    print("Type 'quit' or press Ctrl+C to exit.\n")
    
    # A few sample URLs to try if you don't have one handy
    print("💡 Sample image URLs to try:")
    print("   https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800")
    print("   https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800")
    print("   https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800")
    print()

    while True:
        try:
            # Get image URL from user
            image_url = input("📸 Enter food image URL: ").strip()
            
            # Exit conditions
            if image_url.lower() in ["quit", "exit", "q", ""]:
                print("\n👋 Thanks for using AI Food Analyzer! Stay healthy!")
                break
            
            # Basic URL validation
            if not image_url.startswith("http"):
                print("⚠️  Please enter a valid URL starting with http:// or https://\n")
                continue
            
            # Run the analysis
            result = analyze_food_image(image_url)
            
            # Print a clean divider then the result
            print("\n" + "─" * 55)
            print(result)
            print("─" * 55 + "\n")
            
            # Ask if they want to analyze another
            again = input("🔄 Analyze another image? (y/n): ").strip().lower()
            if again != "y":
                print("\n👋 Thanks for using AI Food Analyzer! Stay healthy!")
                break
            print()

        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using AI Food Analyzer! Stay healthy!")
            break


# Entry point
if __name__ == "__main__":
    main()
