import re
from random import shuffle

import scrapy
from requests_html import HTMLSession
from scrapy.http.request import Request
from scrapy.loader import ItemLoader

from ..detaconn import (deta_doi_to_local_disk, deta_get_doi,
                        deta_get_unscraped_doi, deta_put_abstract,
                        deta_put_scraped_flag,
                        deta_unscraped_doi_to_local_disk, doi_from_local_disk)
from ..items import ScrapeAshItem

session = HTMLSession()


def google_lat_lon(query: str):

    url = "https://www.google.com/maps/search/?api=1"
    params = {}
    params["query"] = query

    r = session.get(url, params=params)

    reg = "APP_INITIALIZATION_STATE=[[[{}]"
    res = r.html.search(reg)[0]
    lat = res.split(",")[2]
    lon = res.split(",")[1]

    return lat, lon


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def remove_intr_by(string: str) -> str:
    clean_str = re.sub("\(Intr\..*?\)", "", string)
    return clean_str


class AbstractSpider(scrapy.Spider):
    name = "abstracts"
    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        # pass in the following as -a arguments to scrapy crawl
        # anything other than "False" will evaluate as True

        clean_scrape = self.clean_scrape
        get_url_from_web = self.get_url_from_web
        get_doi_from_disk = self.get_doi_from_disk

        if clean_scrape == "False":
            clean_scrape = False
        if get_url_from_web == "False":
            get_url_from_web = False
        if get_doi_from_disk == "False":
            get_doi_from_disk = False

        print(
            f"""
        clean_scrape: {clean_scrape} {type(clean_scrape)}, 

        get_url_from_web: {get_url_from_web} {type(get_url_from_web)}, 

        get_doi_from_disk: {get_doi_from_disk} {type(get_doi_from_disk)},
                """
        )

        if clean_scrape:
            start_urls = deta_get_doi()
            deta_doi_to_local_disk(start_urls)

        elif get_url_from_web:
            start_urls = deta_get_unscraped_doi()
            deta_unscraped_doi_to_local_disk(start_urls)

        elif get_doi_from_disk:
            start_urls = doi_from_local_disk()

            # Next part was to add flags, hopefully only have to do once
            # chunked = list(chunks(start_urls, 25))
            # for urls in chunked:
            #     deta_put_scraped_flag(urls)

            # until I get the code for selecting unscraped URLs working...
            shuffle(start_urls)

        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        l = ItemLoader(item=ScrapeAshItem(), response=response)

        l.add_css("key", "div.citation-doi a::attr(href)")
        l.add_css("doi", "div.citation-doi a::attr(href)")
        l.add_css("article_title", "h1.wi-article-title.article-title-main ::text")
        l.add_css("article_date", "span.article-date")
        l.add_css("session_type", "span.article-client_type")
        l.add_css("abstract_text", "section.abstract ::text")
        l.add_css("topics", "div.content-metadata-topics a::text")
        l.add_css("author_names", "a.linked-name ::text")

        authors = response.css("div.info-card-author")
        author_affiliation_list = []
        for author in authors:
            authors_affils = author.css("div.aff::text").getall()
            # clean out the "(Intr. by)" nonsense
            authors_affils = [remove_intr_by(a) for a in authors_affils]
            # if that resulted in an empty string, remove it
            authors_affils = list(filter(None, authors_affils))
            author_affiliation_list.append(authors_affils)

        l.add_value("author_affiliations", author_affiliation_list)

        first_author_affiliation = author_affiliation_list[0]
        # handle getting the first affiliation if author has multiple affiliations
        if isinstance(first_author_affiliation, list):
            first_author_affiliation = first_author_affiliation[0]
        lat, lon = google_lat_lon(first_author_affiliation)
        l.add_value("first_author_latitude", lat)
        l.add_value("first_author_longitude", lon)
        l.add_value("is_scraped", "1")

        # print(dict(l.load_item()))
        deta_put_abstract(dict(l.load_item()))

        yield l.load_item()
