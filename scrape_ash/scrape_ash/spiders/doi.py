import scrapy
from scrapy.loader import ItemLoader
from scrapy.http.request import Request
import datetime
from sqlite_utils import Database
import sqlite3

from ..items import ScrapeAshURL
from ..pipelines import URLS_DB_PATH, URLS_TABLE_NAME

class DOISpider(scrapy.Spider):
    name = "dois"
    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        search_url = "https://ashpublications.org/blood/search-results"
        search_string = "?sort=Date+-+Oldest+First&f_ArticleTypeDisplayName=Meeting+Report&fl_SiteID=1000001&page="
        try:
            db = Database(URLS_DB_PATH)
            q = db.execute(f"select MAX(start_url_page_num) from {URLS_TABLE_NAME}").fetchall() 
            start_url_page = int(q[0][0]) # execute command returns a list of tuples of strings
        except sqlite3.OperationalError:
            start_url_page = 1

        # the last page last scraped might not be full,
        # so go back one page to make sure
        # we're not missing any new items

        if start_url_page > 4000:
            start_url_page = start_url_page - 1
            print(f"Starting scraping at page {start_url_page}.")

        start_urls = [f"{search_url}{search_string}{start_url_page}"]
        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):

        selector = "div.sr-list.al-article-box.al-normal.clearfix.content-type-journal-articles"
        link_selection = response.css(selector)

        for link in link_selection:

            il = ItemLoader(item=ScrapeAshURL(), selector=link)

            search_url = response.url
            start_url_page_num =  search_url.split("page=", 1)[1]
            url = response.urljoin(link.css("div.sri-title.customLink.al-title a::attr(href)").get())
            datetime_link_obtained = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

            il.add_value("search_url", search_url)
            il.add_value("start_url_page_num", start_url_page_num)
            il.add_css("doi", "div.citation-label a::attr(href)")
            il.add_value("url", url)
            il.add_value("datetime_link_obtained", datetime_link_obtained)
            il.add_value("is_scraped", "0")

            payload = il.load_item()

            yield payload


        next_page = (
            "search-results?" + response.css("a.sr-nav-next::attr(data-url)").get()
        )

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
