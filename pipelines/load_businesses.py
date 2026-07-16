import pandas as pd
from database.db import engine

df = pd.read_csv("configs/business.csv")

df.to_sql(
    "business",
    engine,
    if_exists="append",
    index=False
)

print (f"loaded {len(df)} businesses")

df = pd.read_csv("configs/business_alias.csv")

df.to_sql(
    "business_alias",
    engine,
    if_exists="append",
    index=False
)