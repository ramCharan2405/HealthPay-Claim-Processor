import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure_genai():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    genai.configure(api_key=api_key)

async def generate_content(prompt: str) -> str:
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await model.generate_content_async(prompt)
    return response.text
