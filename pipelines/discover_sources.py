from ddgs import DDGS
from urllib.parse import urlparse
import pandas as pd
from database.db import engine
from sqlalchemy import text

'''
HELPER FUNCTIONS
'''
def search (query, max_results=10):
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))

def classify(url):
    domain = urlparse(url).netloc.lower()

    if "reddit.com" in domain:
        return "reddit"
    if "amazon.com" in domain:
        return "amazon"
    if "walmart.com" in domain:
        return "walmart"
    
    return "website"


# populate discovered_source table

search_seeds = pd.read_sql("""
    SELECT
        seed_id,
        business_id,
        source_type,
        seed_text,
        seed_type
    FROM business_search_seed                        
""", engine)

rows = []

for _, seed in search_seeds.iterrows():

    results = search(seed["seed_text"])
    
    for rank, result in enumerate(results, start=1):
        rows.append({
            "business_id": seed["business_id"],
            "seed_id": seed["seed_id"],
            "url": result["href"],
            #"domain": result["href"].split("/")[2],
            "source_type": classify(result["href"]),
            "title": result["title"],
            "snippet": result["body"],
            "rank": rank
        })

# insert in SQL
discovered_df = pd.DataFrame(rows)

discovered_df = discovered_df.drop_duplicates(subset=["business_id", "url"])

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE discovered_source RESTART IDENTITY;"))

discovered_df.to_sql(
    "discovered_source",
    engine,
    if_exists="append",
    index=False
)