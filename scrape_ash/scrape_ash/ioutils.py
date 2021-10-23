import json
import os
from pathlib import Path
from urllib.parse import quote_plus, urlparse

import requests
from scrapy.http import Response

doi_json_path = "data/doi_json"


def doi_json_fname(doi_link: str):
    url_path = urlparse(doi_link).path

    # remove leading slash if it exists
    if url_path.startswith("/"):
        url_path = url_path[1:]

    fname = quote_plus(url_path)

    return fname


def get_start_url_page():
    start_url_page = os.getenv("START_URL_PAGE_NUM")
    if start_url_page:
        start_url_page = int(start_url_page)
    else:
        start_url_page = 1

    return start_url_page


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


def get_unscraped():
    url = "https://ash-abstracts.vercel.app/abstracts/abstracts.json?_sort=doi&is_scraped__exact=0&_shape=array"
    res = requests.get(url=url)
    l = res.json()
    with open("unscraped.json", "w") as f:
        json.dump(l, f, indent=4)

    doi_list = [d["doi"] for d in l]

    return doi_list


def get_doi_dict(doi: str):
    with open("unscraped.json", "r") as f:
        doi_dict_list = json.load(f)
    for doi_dict in doi_dict_list:
        if doi_dict["doi"] == doi:
            d = doi_dict

    return d


def mk_abstract_json(abstract_dict: dict, doi_json_path: str = doi_json_path):
    doi = abstract_dict["doi"]

    p = doi_json_path
    fname = doi_json_fname(doi_link=doi)
    f_path = f"{p}/{fname}.json"

    doi_dict = get_doi_dict(doi)

    abstract_dict = doi_dict | abstract_dict

    with open(f_path, "w") as f:
        json.dump(abstract_dict, f, indent=4)

    return abstract_dict
