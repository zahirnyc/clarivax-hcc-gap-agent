from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a Medicare Risk Adjustment expert."},
        {"role": "user", "content": "What is HCC code 19 and what ICD-10 codes map to it?"}
    ]
)

print(response.choices[0].message.content)