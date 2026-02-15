import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

VECTOR_DB_PATH = "./knowledge_base"

SIMILARITY_THRESHOLD = 0.90
MAX_CHUNKS = 5000