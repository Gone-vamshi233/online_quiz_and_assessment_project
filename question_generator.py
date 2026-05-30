from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt = """
Generate 5 Python MCQs.

Return ONLY valid JSON.

Format:

[
 {
   "question":"...",
   "option_a":"...",
   "option_b":"...",
   "option_c":"...",
   "option_d":"...",
   "answer":"A"
 }
]
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)