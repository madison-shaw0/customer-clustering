import pandas as pd
from database.db import engine
from sqlalchemy import text

#PURPOSE: used for initializing search seeds table

#read businesses and business aliases from tables
businesses = pd.read_sql("""
                          SELECT b.business_id,
                                  b.display_name AS search_name
                          FROM business b
                         
                          UNION
                         
                          SELECT a.business_id,
                                a.alias_text AS search_name
                          FROM business_alias a

                          """, engine)


#recipe for generating searches (search, pattern, type)
#TODO: Move this to csv
SEARCH_PATTERNS = [
    ("reddit", "{name} reddit", "reddit"),
    ("web", "{name} reviews", "review"),
    ("web", "{name} complaints", "complaint"),
    ("web", "{name} forum", "forum"),
    ("web", "{name} alternatives", "alternative"),
    ("web", "{name} vs", "comparison"),
]

rows = []

for _, business in businesses.iterrows():
    for source, pattern, seed_type in SEARCH_PATTERNS:
        rows.append({
            "business_id": business["business_id"],
            "source_type": source,
            "seed_text": pattern.format(name=business["search_name"]),
            "seed_type": seed_type
        })

seed_df = pd.DataFrame(rows)

#clear table to avoid duplicate rows
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE business_search_seed RESTART IDENTITY;"))

seed_df.to_sql(
    "business_search_seed",
    engine,
    if_exists="append",
    index=False
)