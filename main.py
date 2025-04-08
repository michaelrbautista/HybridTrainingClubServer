from typing import Literal
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
RESEND_API_KEY = os.getenv('RESEND_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is missing.")

client = OpenAI(api_key=OPENAI_API_KEY)

class Workout(BaseModel):
    type: Literal["easy run", "speed workout", "long run", "upper body lift", "lower body lift"]

class Day(BaseModel):
    day: Literal["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    workouts: List[Workout]

class Week(BaseModel):
    days: List[Day]

# uvicorn main:app --reload

@app.post("/week")
def post_program():
    return create_weekly_structure()

def create_weekly_structure():
    print("Creating structure...")
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "You are a professional strength and conditioning coach."
            },
            {
                "role": "user",
                "content": """
                Create a weekly training schedule following these rules exactly:
1. Include exactly one long run on Sunday.
2. Do not include any runs Monday.
3. Include exactly one speed workout on Thursday.
4. Include exactly five easy runs. Do not schedule any runs on Monday.
                """
            }
        ],
        response_format=Week
    )
    return completion.choices[0].message.content
