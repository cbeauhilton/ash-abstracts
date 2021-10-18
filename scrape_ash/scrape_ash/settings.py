BOT_NAME = "scrape_ash"

SPIDER_MODULES = ["scrape_ash.spiders"]
NEWSPIDER_MODULE = "scrape_ash.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS = 2  # don't get kicked out! Default 16.
CLOSESPIDER_PAGECOUNT = 2 # limit number of scraped pages per crawl

ITEM_PIPELINES = {
    "scrape_ash.pipelines.AbstractPipeline": 300,
}

DUPEFILTER_DEBUG = True
