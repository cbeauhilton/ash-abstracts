import os
import json
import scrapy
from scrapy.http.request import Request
from scrapy.http import Response
from scrapy.utils.conf import closest_scrapy_cfg

from ..detaconn import (deta_get_start_url_page, deta_put_doi,
                        deta_put_start_url)

from urllib.parse import quote_plus
from urllib.parse import urlparse
from pathlib import Path


def mk_json(doi_link: str, response: Response):
        # make a json file as well
        d = {}
        d["doi"] = doi_link
        d["start_url"] = response.request.url
        d["is_scraped"] = 0

        url_path = urlparse(doi_link).path
        fname = quote_plus(url_path)
        print(os.getcwd())

        p = f"scrape_ash/data/doi_json"
        Path(p).mkdir(parents=True, exist_ok=True)

        with open(f"{p}/{fname}") as f:
            json.dump(d, f)

        return d

class DOISpider(scrapy.Spider):
    name = "dois"
    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        search_url = "https://ashpublications.org/blood/search-results"
        search_string = "?sort=Date+-+Oldest+First&f_ArticleTypeDisplayName=Meeting+Report&fl_SiteID=1000001&page="
        try:
            start_url_page = deta_get_start_url_page()
        except Exception as e:
            print(e)
            start_url_page = 1

        clean_scrape = self.clean_scrape

        if clean_scrape == "False":
            clean_scrape = False

        if clean_scrape:
            start_url_page = 1

        # the last page last scraped might not be full,
        # so go back a couple of pages to make sure
        # we're not missing any new items
        # (it would probably be sufficient to go back one page)

        if start_url_page > 10:
            start_url_page = start_url_page - 2
            print(f"Starting scraping at page {start_url_page}.")

        start_urls = [f"{search_url}{search_string}{start_url_page}"]
        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        for link in response.css("div.citation-label a::attr(href)"):
            doi_link = link.get()
            deta_put_doi(doi_link)

            # make json as well
            d = mk_json(doi_link=doi_link, response=response)
            print(d)


        # save the url of the current page to a deta instance,
        # will be queried on subsequent runs to avoid re-scraping
        deta_put_start_url(response)

        next_page = (
            "search-results?" + response.css("a.sr-nav-next::attr(data-url)").get()
        )

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
