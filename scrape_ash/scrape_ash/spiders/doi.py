import scrapy
from scrapy.http.request import Request

from ..detaconn import (deta_get_start_url_page, deta_put_doi,
                        deta_put_start_url)

# from scrapy.crawler import CrawlerProcess


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

        # save the url of the current page to a deta instance,
        # will be queried on subsequent runs to avoid re-scraping
        deta_put_start_url(response)

        next_page = (
            "search-results?" + response.css("a.sr-nav-next::attr(data-url)").get()
        )

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


# process = CrawlerProcess()
# process.crawl(DOISpider)
# process.start()
