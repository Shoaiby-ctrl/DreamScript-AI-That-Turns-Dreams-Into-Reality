import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")

# Configure Gemini
genai.configure(api_key=api_key)

# Test with a simple prompt
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Hello Gemini! Can you say hi?")
print("✅ Gemini Response:", response.text)
