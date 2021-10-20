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
    d["start_url_page_num"] = d["start_url"].split("page=", 1)[1]
    d["is_scraped"] = 0

    p = doi_json_path
    Path(p).mkdir(parents=True, exist_ok=True)

    fname = doi_json_fname(doi_link=doi_link)

    with open(f"{p}/{fname}.json", "w") as f:
        json.dump(d, f, indent=4)

    return d


def get_start_url_page(doi_json_path: str = doi_json_path):
    json_files = [j for j in os.listdir(doi_json_path) if j.endswith(".json")]
    json_dicts = []
    for _, js in enumerate(json_files):
        with open(os.path.join(doi_json_path, js)) as json_file:
            json_dicts.append(json.load(json_file))
    pages = [d["start_url"].split("page=", 1)[1] for d in json_dicts]
    pages = [int(p) for p in list(set(pages)) if p != "None"]
    len_pages = len(pages)
    max_pages = max(pages)
    print(f"Total number of scraped pages: {len_pages}")
    if len_pages < max_pages:
        print(
            f"len_pages != max_pages : len_pages = {len_pages}, max_pages = {max_pages}"
        )
    start_url_page = max_pages
    return start_url_page
