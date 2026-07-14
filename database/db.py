from sqlalchemy import create_engine
from urllib.parse import quote_plus

USERNAME = "postgres"
PASSWORD = quote_plus("RomRan9@9@")
HOST = "localhost"
PORT = "5432"
DATABASE = "customer_clustering"

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

with engine.connect() as conn:
    print("Connected")