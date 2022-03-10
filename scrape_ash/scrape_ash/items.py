import scrapy
from itemloaders.processors import Join, MapCompose
from w3lib.html import remove_tags


class ScrapeAshItem(scrapy.Item):

    doi = scrapy.Field(output_processor=Join())
    link = scrapy.Field(output_processor=Join())

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

    first_author_latitude = scrapy.Field(output_processor=Join())

    first_author_longitude = scrapy.Field(output_processor=Join())

    is_scraped = scrapy.Field(output_processor=Join())


class ScrapeAshLink(scrapy.Item):

    search_url = scrapy.Field(output_processor=Join())

    doi = scrapy.Field(output_processor=Join())

    url = scrapy.Field(output_processor=Join())

    datetime_link_obtained = scrapy.Field(output_processor=Join())

    is_scraped = scrapy.Field(output_processor=Join())
