import random
import json
from urllib.parse import quote_plus, urlparse

import requests


def doi_json_fname(doi_link: str):
    url_path = urlparse(doi_link).path

    # remove leading slash if it exists
    if url_path.startswith("/"):
        url_path = url_path[1:]

    fname = quote_plus(url_path)

    return fname


def get_unscraped():
    # select from db randomly 
    # so that the same screwy links that don't work won't puddle as much
    url = "https://ash-unscraped.vercel.app/unscraped.json?sql=SELECT%20*%20FROM%20unscraped%20WHERE%20%22is_scraped%22%20%3D%20%3Ap0%20AND%20doi%20IN%20(SELECT%20doi%20FROM%20unscraped%20ORDER%20BY%20RANDOM()%20LIMIT%20500)&p0=0&_shape=array"
    url = "https://ash-abstracts.vercel.app/abstracts/abstracts.json?_shape=array"
    res = requests.get(url=url)
    l = res.json()
    with open("unscraped.json", "w") as f:
        json.dump(l, f, indent=4)

    doi_list = [d["doi"] for d in l]

    # and another randomization for good measure
    random.shuffle(doi_list)

    return doi_list


def get_doi_dict(doi: str):
    d = None
    with open("unscraped.json", "r") as f:
        doi_dict_list = json.load(f)
    for doi_dict in doi_dict_list:
        if doi_dict["doi"] == doi:
            d = doi_dict

    return d
