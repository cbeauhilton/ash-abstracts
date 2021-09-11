from urllib.parse import quote_plus

import scrapy
from itemloaders.processors import Join, MapCompose
from w3lib.html import remove_tags


class ScrapeAshItem(scrapy.Item):
    key = scrapy.Field(input_processor=MapCompose(quote_plus), output_processor=Join())

    doi = scrapy.Field(output_processor=Join())

    article_title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip), output_processor=Join()
    )

    article_date = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip), output_processor=Join()
    )

    session_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip), output_processor=Join()
    )

    abstract_text = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip), output_processor=Join()
    )

    topics = scrapy.Field()

    author_names = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip))

    author_affiliations = scrapy.Field()

    first_author_latitude = scrapy.Field()

    first_author_longitude = scrapy.Field()
