import os
import json
import scrapy
from scrapy.http.request import Request
from scrapy.http import Response

from ..detaconn import (deta_get_start_url_page, deta_put_doi,
                        deta_put_start_url)

from urllib.parse import quote_plus
from urllib.parse import urlparse
from pathlib import Path

doi_json_path = "data/doi_json"

def mk_json(doi_link: str, response: Response, doi_json_path: str):
        d = {}
        d["doi"] = doi_link
        d["start_url"] = response.request.url
        d["is_scraped"] = 0

        p = doi_json_path
        Path(p).mkdir(parents=True, exist_ok=True)

        url_path = urlparse(doi_link).path

        # remove leading slash if it exists
        if url_path.startswith('/'):
            url_path = url_path[1:]

        fname = quote_plus(url_path)

        with open(f"{p}/{fname}.json", "w") as f:
            json.dump(d, f)

        return d

def get_start_url_page(doi_json_path: str):
    json_files = [j for j in os.listdir(doi_json_path) if j.endswith('.json')]
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
        print(f"len_pages != max_pages : len_pages = {len_pages}, max_pages = {max_pages}")
    start_url_page = max_pages
    return start_url_page

class DOISpider(scrapy.Spider):
    name = "dois"
    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        search_url = "https://ashpublications.org/blood/search-results"
        search_string = "?sort=Date+-+Oldest+First&f_ArticleTypeDisplayName=Meeting+Report&fl_SiteID=1000001&page="
        try:
            # start_url_page = deta_get_start_url_page()
            start_url_page = get_start_url_page(doi_json_path)
        except Exception as e:
            print(e)
            start_url_page = 1

        clean_scrape = self.clean_scrape

        if clean_scrape == "False":
            clean_scrape = False

        if clean_scrape:
            start_url_page = 1

        # the last page last scraped might not be full,
        # so go one page to make sure
        # we're not missing any new items

        if start_url_page > 10:
            start_url_page = start_url_page - 1
            print(f"Starting scraping at page {start_url_page}.")

        start_urls = [f"{search_url}{search_string}{start_url_page}"]
        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        for link in response.css("div.citation-label a::attr(href)"):
            doi_link = link.get()
            # deta_put_doi(doi_link)

            d = mk_json(doi_link=doi_link, response=response, doi_json_path=doi_json_path)
            print(d)


        # save the url of the current page to a deta instance,
        # will be queried on subsequent runs to avoid re-scraping
        # deta_put_start_url(response)

        next_page = (
            "search-results?" + response.css("a.sr-nav-next::attr(data-url)").get()
        )

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
