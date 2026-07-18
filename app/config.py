"""Reads environment variables (database URL, base URL for shortened links, default TTL, etc.)
 into a single settings object, usually via pydantic-settings. 
 Every other file imports settings from here instead of reading os.environ directly.
"""
from dotenv import load_dotenv
import os
load_dotenv()

host=os.getenv("DB_HOST")
port=os.getenv("DB_PORT")
dbname=os.getenv("DB_NAME")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
DATABASE_URL = (f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}")
