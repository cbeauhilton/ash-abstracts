from itemadapter import ItemAdapter

from sqlite_utils import Database
import json
from pathlib import Path
from urllib.parse import quote_plus, urlparse

DATA_PATH = "data"
DOI_JSON_PATH = f"{DATA_PATH}/doi_json"
URLS_DB_PATH = f"{DATA_PATH}/urls.db"
URLS_TABLE_NAME = "urls" 
ABSTRACTS_DB_PATH = f"{DATA_PATH}/abstracts.db"
ABSTRACTS_TABLE_NAME = "abstracts"
        
def doi_json_fname(doi_link: str):
    url_path = urlparse(doi_link).path
    # remove leading slash if it exists
    if url_path.startswith("/"):
        url_path = url_path[1:]
    fname = quote_plus(url_path)
    return fname


class JsonWriterPipeline:

    def __init__(self):
        self.p = DOI_JSON_PATH
        Path(self.p).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        fname = doi_json_fname(doi_link=item_dict["doi"])
        json_file = f"{self.p}/{fname}.json"
        with open(json_file, "w") as f:
            json.dump(item_dict, f, indent=4)
        return item


class SQLitePipeline:

    def __init__(self):
        self.urls_db = Database(URLS_DB_PATH)
        self.urls_table_name = URLS_TABLE_NAME
        self.abstracts_db = Database(ABSTRACTS_DB_PATH)
        self.abstracts_table_name = ABSTRACTS_TABLE_NAME

    def process_item(self, item, spider):
        if spider.name == "dois":
            db, table  = self.urls_db, self.urls_table_name
        elif spider.name == "abstracts":
            db, table = self.abstracts_db, self.abstracts_table_name

        db[table].upsert(ItemAdapter(item).asdict(), pk="doi", alter=True)

        if spider.name == "abstracts":
            db, table  = self.urls_db, self.urls_table_name
            db[table].update(ItemAdapter(item).asdict()["doi"], {"is_scraped": "1"} )

        return item

    def close_spider(self, spider):
        self.urls_db.enable_counts()
        self.abstracts_db.enable_counts() 
        # col_list = [*self.abstracts_db[self.abstracts_table_name].columns_dict]
        # unwanted_cols_list = ["search_url", "doi", "url", "datetime_link_obtained", "is_scraped", "start_url_page_num"]
        # fts_cols_list = [x for x in col_list if x not in unwanted_cols_list]
        # print("\n"*10)
        # print(col_list)
        # print(unwanted_cols_list)
        # print(fts_cols_list)
        # print("\n"*10)
        # self.abstracts_db[self.abstracts_table_name].enable_fts(fts_cols_list, create_triggers=True) 
        # self.abstracts_db[self.abstracts_table_name].optimize() 
