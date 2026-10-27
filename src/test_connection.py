import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Loading the values from .env
load_dotenv(override=True)

# Read each value by its NAME in .env
user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

# Building the connection string
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Creating the engine
engine = create_engine(url)

# 5. Connect and test
with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print("Connected!")
    print(result.scalar())