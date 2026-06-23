import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found!")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Generate response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello, are you working?"
)

print("\nGemini Response:\n")
print(response.text)