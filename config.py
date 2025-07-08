# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

COUNTRY = "in"
DEFAULT_QUERY = "data scientist"
DEFAULT_LOCATION = "bangalore"

SKILLS_LIST = [
    "python", "sql", "tableau", "power bi", "pandas", "numpy", "scikit-learn",
    "tensorflow", "keras", "pytorch", "aws", "azure", "docker", "kubernetes",
    "nlp", "machine learning", "deep learning", "big data", "hadoop", "spark"
]
