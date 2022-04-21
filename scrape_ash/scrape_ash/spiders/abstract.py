import re

import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from sqlite_utils import Database

from ..items import ScrapeAshItem
from ..pipelines import URLS_DB_PATH, URLS_TABLE_NAME


def remove_intr_by(string: str) -> str:
    clean_str = re.sub("\(Intr\..*?\)", "", string)
    return clean_str


class AbstractSpider(scrapy.Spider):
    name = "abstracts"

    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        db = Database(URLS_DB_PATH)
        q = db.execute(f"select url from {URLS_TABLE_NAME} where is_scraped = ?", "0").fetchall() 
        start_urls = [x[0] for x in q]

        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        l = ItemLoader(item=ScrapeAshItem(), response=response)

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

        l.add_css("doi", "div.citation-doi a::attr(href)")
        l.add_css("article_title", "h1.wi-article-title.article-title-main ::text")
        l.add_css("article_date", "span.article-date")
        l.add_css("session_type", "span.article-client_type")
        l.add_css("abstract_text", "section.abstract ::text")
        l.add_css("topics", "div.content-metadata-topics a::text")
        l.add_css("author_names", "a.linked-name ::text")
        l.add_value("author_dict_list", author_dict_list)
        l.add_value("is_scraped", "1")

        abstract_object = l.load_item()

        yield abstract_object
