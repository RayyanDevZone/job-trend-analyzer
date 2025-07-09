# from dotenv import load_dotenv
import os

# load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

DEFAULT_QUERY = "data scientist"
DEFAULT_LOCATION = "Bangalore"

COUNTRY_CODES = {
    "India": "in",
    "Australia": "au",
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
}

SKILLS_LIST = [
    "python", "sql", "tableau", "power bi", "pandas", "numpy", "scikit-learn",
    "tensorflow", "keras", "pytorch", "aws", "azure", "docker", "kubernetes",
    "nlp", "machine learning", "deep learning", "big data", "hadoop", "spark"
]
