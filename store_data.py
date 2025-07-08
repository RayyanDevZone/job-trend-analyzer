import pandas as pd
from sqlalchemy import create_engine

# Load your cleaned data
df = pd.read_csv("jobs_data_cleaned.csv")

# Your Neon PostgreSQL connection string
DB_URL = "postgresql://neondb_owner:npg_g2bYdt1XEeuD@ep-fragrant-math-adwk6g26-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Create engine
engine = create_engine(DB_URL)

# Upload the data to a table
df.to_sql("job_listings", engine, if_exists="replace", index=False)

print("✅ Data uploaded to Neon PostgreSQL!")
