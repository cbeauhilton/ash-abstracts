from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .detaconn import deta_put_abstract


class AbstractPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not adapter.get("abstract_text"):
            raise DropItem(f"{item} is missing the abstract, will not save.")

        names_len = len(adapter.get("author_names"))
        aff_len = len(adapter.get("author_affiliations"))
        if names_len != aff_len:
            raise DropItem(
                f"Length of author list and affiliation list are not equal in {item}."
            )
        else:
            deta_put_abstract(adapter.asdict())
            return item
