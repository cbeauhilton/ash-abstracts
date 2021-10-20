import scrapy
from scrapy.http.request import Request

from ..ioutils import get_start_url_page, mk_doi_json


class DOISpider(scrapy.Spider):
    name = "dois"
    allowed_domains = ["ashpublications.org", "doi.org"]

    def start_requests(self):
        search_url = "https://ashpublications.org/blood/search-results"
        search_string = "?sort=Date+-+Oldest+First&f_ArticleTypeDisplayName=Meeting+Report&fl_SiteID=1000001&page="
        try:
            start_url_page = get_start_url_page()
        except Exception as e:
            print(f"Could not get start_url_page, exception: {e}")
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

            mk_doi_json(doi_link=doi_link, response=response)

        next_page = (
            "search-results?" + response.css("a.sr-nav-next::attr(data-url)").get()
        )

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
