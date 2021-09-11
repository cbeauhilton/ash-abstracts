# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .detaconn import deta_put_abstract


class AbstractPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        names_len = len(adapter.get("author_names"))
        aff_len = len(adapter.get("author_affiliations"))
        if names_len != aff_len:
            raise DropItem(
                f"Length of author list and affiliation list are not equal in {item}."
            )
        else:
            deta_put_abstract(adapter.asdict())
            return item


# class DOIPipeline:
#         def open_spider(self, spider):
#             self.file = open('items.jl', 'w')

#         def close_spider(self, spider):
#             self.file.close()
