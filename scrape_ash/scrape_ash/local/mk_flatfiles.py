import json
from pathlib import Path

import dateparser
from sqlite_utils import Database

db = Database("../data/base.db")
date_col_name = "article_date"
years = []

for row in db["abstracts_base"].rows:
    date = str(row[date_col_name])
    dt = dateparser.parse(date)
    years.append(dt.year)

years = list(set(years))
for year in years:
    path = f"../data/json/{year}"
    Path(path).mkdir(parents=True, exist_ok=True)
    query = f"select * from abstracts_base where {date_col_name} LIKE '%{year}%'"
    for row in db.query(query):
        file = f"{path}/{row['key']}.json"
        with open(file, "w") as f:
            json.dump(row, f, indent=4)
