import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY is not None, "❌ OPENAI_API_KEY is not set!"

# Database configuration

# logging configuration