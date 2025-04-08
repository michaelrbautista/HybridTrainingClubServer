from typing import Literal
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import uvicorn

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
    type: Literal["easy run", "speed workout", "long run", "lower body lift", "upper body lift"]

class Day(BaseModel):
    day: Literal["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    workouts: List[Workout]

class Week(BaseModel):
    days: List[Day]

@app.get("/")
async def read_root():
    return {"message": "FastAPI app is running."}

@app.head("/")
async def head_root():
    return {"message": "FastAPI app is running."}

# uvicorn main:app --reload

@app.post("/week")
def post_program():
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
1. Include one long endurance session on Saturday.
2. Include one quality endurance session three days before Saturday.
3. Include 5 easy endurance sessions throughout the week. Include multiple sessions a day if needed.
4. Include 1 lower body lift and 1 upper body lift.
5. Do not schedule any workouts on Wednesday or Friday. Move any workouts on these days accordingly.
                """
            }
        ],
        response_format=Week
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Default to 10000 if not set
    uvicorn.run(app, host="0.0.0.0", port=port)
