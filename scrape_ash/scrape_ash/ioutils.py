import json
import os
from pathlib import Path
from urllib.parse import quote_plus, urlparse

from scrapy.http import Response

doi_json_path = "data/doi_json"


def doi_json_fname(doi_link: str):
    url_path = urlparse(doi_link).path

    # remove leading slash if it exists
    if url_path.startswith("/"):
        url_path = url_path[1:]

    fname = quote_plus(url_path)

    return fname


def mk_doi_json(doi_link: str, response: Response, doi_json_path: str = doi_json_path):
    d = {}
    d["doi"] = doi_link
    d["start_url"] = response.request.url
    d["start_url_page_num"] = int(d["start_url"].split("page=", 1)[1])
    d["is_scraped"] = 0

    p = doi_json_path
    Path(p).mkdir(parents=True, exist_ok=True)

    fname = doi_json_fname(doi_link=doi_link)

    with open(f"{p}/{fname}.json", "w") as f:
        json.dump(d, f, indent=4)

    return d


def mk_abstract_json(abstract_dict: dict, doi_json_path: str = doi_json_path):
    p = doi_json_path
    fname = doi_json_fname(doi_link=abstract_dict["doi"])
    f_path = f"{p}/{fname}.json"
    print(fname)

    with open(f_path, "r") as f:
        doi_dict = json.load(f)

    abstract_dict = doi_dict | abstract_dict

    with open(f_path, "w") as f:
        print(f_path)
        print(abstract_dict)
        # json.dump(abstract_dict, f, indent=4)

    return abstract_dict

def get_start_url_page():
    start_url_page = os.getenv("START_URL_PAGE_NUM")
    if start_url_page:
        start_url_page = int(start_url_page)
    else:
        start_url_page = 1

    return start_url_page
