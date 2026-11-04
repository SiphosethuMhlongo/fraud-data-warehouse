import os
import pandas as pd
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(override=True)
user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(url)

csv_file_path=  r"C:\Users\sethu\Downloads\PS_20174392719_1491204439457_log.csv"
print("Reading the CSV this might take a minute")
df =pd.read_csv(csv_file_path)
print(f"Done rowes loaded into memory:{len(df)}")

print("uploading to postgreSQL..this will take a few minutes")
df.to_sql(
    name='stg_transactions', 
    con=engine, 
    if_exists='replace', 
    index=False, 
    chunksize=10000, 
    method='multi'
)
print ("Upload completed")

print("Verifying row count")
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM stg_transactions;"))
    db_row_count = result.scalar()
    print(f"   Rows in database: {db_row_count}")

if db_row_count == len(df):
    print("SUCCESS! CSV and Database row counts match.")
else:
    print("WARNING! Row counts do not match.")