import json
import os
from typing import List
from urllib.parse import quote_plus

from deta import Deta
from scrapy.http import Response
from tenacity import retry
from tenacity.stop import stop_after_attempt

from .timeout import dynamic_timeout

project_id = os.environ.get("DETA_ID_ASH")
API_key = os.environ.get("DETA_TOKEN_ASH")
deta = Deta(API_key)


@retry(
    stop=stop_after_attempt(500),
    after=dynamic_timeout(20),
    before=dynamic_timeout(20),
)
def deta_get_all(detabase: str) -> List[dict]:
    db = deta.Base(detabase)
    grab = db.fetch(limit=50)  # the limit only applies to the first fetch
    response = grab.items

    while grab.last:
        grab = db.fetch(last=grab.last, limit=1000)
        response += grab.items
        print(len(response))

    return response


def deta_del_list(detabase: str, del_list: list):
    db = deta.Base(detabase)
    for d in del_list:
        db.delete(d)
        print(f"Deleted {d} .")


def deta_get_start_url_page() -> int:
    response = deta_get_all("start_urls")
    pages = [d["start_url"].split("page=", 1)[1] for d in response]
    pages = [int(p) for p in list(set(pages)) if p != "None"]
    print(f"Total number of scraped pages: {len(pages)}")
    start_url_page = max(pages)
    # TODO: code for if len(pages) != max(pages)

    return start_url_page


def deta_put_start_url(response: Response):
    db = deta.Base("start_urls")
    start_url = response.request.url
    # DOIs are already unique, make the URLs into safe strings to create keys
    data = {"key": f"{quote_plus(start_url)}", "start_url": f"{start_url}"}
    db.put(data)


def deta_put_doi(doi: str):
    db = deta.Base("abstracts")
    data = {"key": f"{quote_plus(doi)}", "doi": doi}
    db.put(data)


def deta_clean_doi():
    # accidentally added some junk in early experimentation
    # this probably won't need to be run more than once, ever
    db_name = "abstracts"
    query = {"value?contains": "http"}
    db = deta.Base(db_name)
    grab = db.fetch(query=query)  # the limit only applies to the first fetch
    response = grab.items
    pages = list(set([d["key"] for d in response if "value" in d]))
    print(f"Removing {len(pages)} from {db_name}...")
    deta_del_list(db_name, pages)
    print(f"Removed {len(pages)} from {db_name}.")


def deta_get_doi() -> List[str]:
    response = deta_get_all("abstracts")
    # print(response)
    pages = list(set([d["doi"] for d in response if "doi" in d]))
    print(f"Total number of DOI: {len(pages)}")

    return pages


def deta_doi_to_local_disk(doi: list[str]):
    with open("data/doi.json", "w") as f:
        json.dump(doi, f)


def doi_from_local_disk():
    with open("data/doi.json", "r") as f:
        data = json.load(f)

    return data


def deta_get_unscraped_doi() -> List[str]:
    # TODO: this is not working yet, filtering for missing fields is elusive
    db_name = "abstracts"
    query = {"abstract_text?contains": " "}
    db = deta.Base(db_name)

    grab = db.fetch(query=query)  # the limit only applies to the first fetch
    response = grab.items
    while grab.last:
        try:
            grab = db.fetch(query=query, last=grab.last, limit=1000)
            response += grab.items
            # print(len(response))
            pages = list(set([d["key"] for d in response if "abstract_text" in d]))
            print(pages)
        except:
            print("failure")
            pass

    keys = list(set([d["key"] for d in response]))
    for key in keys:
        query = {"key?ne": "".join(key)}
        print(query)
        grab = db.fetch(query=query, limit=1000)
        response = grab.items
        while grab.last:
            grab = db.fetch(query=query, last=grab.last, limit=1)
            response += grab.items
            print(len(response))
            print(response["key"])

    pages = list(set([d["doi"] for d in response if "doi" in d]))
    print(f"Total number of unscraped DOI: {len(pages)}")

    return pages


def deta_unscraped_doi_to_local_disk(doi: list[str]):
    with open("data/unscraped_doi.json", "w") as f:
        json.dump(doi, f)


def deta_put_abstract(abstract_dict: dict):
    db = deta.Base("abstracts")
    db.put(abstract_dict)
