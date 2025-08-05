import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    Gemini_API_KEY = (
        os.getenv("GEMINI_API_KEY") or
        os.getenv("GOOGLE_API_KEY") or
        os.environ.get("GEMINI_API_KEY") or
        os.environ.get("GOOGLE_API_KEY")
    )
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
