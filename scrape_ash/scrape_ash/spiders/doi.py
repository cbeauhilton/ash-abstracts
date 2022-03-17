import scrapy
from scrapy.loader import ItemLoader
from scrapy.http.request import Request
import datetime

from ..ioutils import get_start_url_page, mk_doi_json
from ..items import ScrapeAshLink

class DOISpider(scrapy.Spider):
    name = "dois"
    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        search_url = "https://ashpublications.org/blood/search-results"
        search_string = "?sort=Date+-+Oldest+First&f_ArticleTypeDisplayName=Meeting+Report&fl_SiteID=1000001&page="
        start_url_page = get_start_url_page()
        start_url_page = 1

        # the last page last scraped might not be full,
        # so go back one page to make sure
        # we're not missing any new items

        if start_url_page > 5:
            start_url_page = start_url_page - 1
            print(f"Starting scraping at page {start_url_page}.")

        start_urls = [f"{search_url}{search_string}{start_url_page}"]
        for url in start_urls:
            yield Request(url, self.parse)

    def parse(self, response):

        selector = "div.sr-list.al-article-box.al-normal.clearfix.content-type-journal-articles"
        link_selection = response.css(selector)

        for link in link_selection:

            il = ItemLoader(item=ScrapeAshLink(), selector=link)

            search_url = response.url
            il.add_value("search_url", search_url)

            il.add_css("doi", "div.citation-label a::attr(href)")

            url = response.urljoin(link.css("div.sri-title.customLink.al-title a::attr(href)").get())
            il.add_value("url", url)

            datetime_link_obtained = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
            il.add_value("datetime_link_obtained", datetime_link_obtained)

            il.add_value("is_scraped", "0")

            payload = il.load_item()
            mk_doi_json(dict(payload))

            yield payload


        next_page = (
            "search-results?" + response.css("a.sr-nav-next::attr(data-url)").get()
        )

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
