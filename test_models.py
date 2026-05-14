
"""Test script to find available Gemini models"""
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

print("Available Models:")
for model in client.models.list():
    print(f"  - {model.name}")
