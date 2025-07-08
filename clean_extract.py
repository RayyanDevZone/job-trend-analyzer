import pandas as pd
import re
from config import SKILLS_LIST

# Step 1: Load the job data
df = pd.read_csv("jobs_data.csv")

# Step 2: Clean job descriptions
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'…+', '', text)                # Remove trailing ellipses
    text = re.sub(r'\s+', ' ', text).strip()      # Remove extra whitespace
    return text

df['clean_description'] = df['description'].apply(clean_text)

# Step 3: Extract skills from descriptions
def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS_LIST if skill in text]

df['skills_found'] = df['clean_description'].apply(extract_skills)

# Step 4: Save enriched data
df.to_csv("jobs_data_cleaned.csv", index=False)
print("Cleaned and enriched data saved to jobs_data_cleaned.csv")
