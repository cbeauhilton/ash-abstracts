import re

import scrapy
from requests_html import HTMLSession
from scrapy.http.request import Request
from scrapy.loader import ItemLoader

from ..ioutils import get_unscraped, mk_abstract_json
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


def remove_intr_by(string: str) -> str:
    clean_str = re.sub("\(Intr\..*?\)", "", string)
    return clean_str


class AbstractSpider(scrapy.Spider):
    name = "abstracts"
    # custom_settings = {
    #         "ITEM_PIPELINES" : {
    # "scrape_ash.pipelines.AbstractPipeline": 300,
    #         }
    #     }

    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):

        start_urls = get_unscraped()

        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        l = ItemLoader(item=ScrapeAshItem(), response=response)

        l.add_css("doi", "div.citation-doi a::attr(href)")
        l.add_css("article_title", "h1.wi-article-title.article-title-main ::text")
        l.add_css("article_date", "span.article-date")
        l.add_css("session_type", "span.article-client_type")
        l.add_css("abstract_text", "section.abstract ::text")
        l.add_css("topics", "div.content-metadata-topics a::text")
        l.add_css("author_names", "a.linked-name ::text")

        author_dict_list = []
        authors = response.css("div.al-author-name")

        for i, author in enumerate(authors):

            author_name = author.css("div.info-card-name::text").get().strip()

            first_author = 0
            last_author = 0
            if i == 0:
                first_author = 1
            if i + 1 == len(authors):
                last_author = 1

            author_affils = author.css("div.aff::text").getall()
            # clean out the "(Intr. by)" nonsense
            author_affils = [remove_intr_by(a) for a in author_affils]
            # if that resulted in an empty string, remove it
            author_affils = list(filter(None, author_affils))

            author_dict = {
                "author_name": author_name,
                "author_affiliations": author_affils,
                "author_rank": i + 1,
                "first_author": first_author,
                "last_author": last_author,
            }

            author_dict_list.append(author_dict)

        l.add_value("author_dict_list", author_dict_list)

        #         first_author_affiliation = author_affiliation_list[0]
        #         # handle getting the first affiliation if author has multiple affiliations
        #         if isinstance(first_author_affiliation, list):
        #             if first_author_affiliation:
        #                 first_author_affiliation = first_author_affiliation[0]
        #             else:
        #                 first_author_affiliation = None

        #         if first_author_affiliation:
        #             lat, lon = google_lat_lon(first_author_affiliation)
        #         else:
        #             lat = None
        #             lon = None

        #         l.add_value("first_author_latitude", lat)
        #         l.add_value("first_author_longitude", lon)

        l.add_value("is_scraped", "1")
        print(l.load_item())

        mk_abstract_json(dict(l.load_item()))

        yield l.load_item()
