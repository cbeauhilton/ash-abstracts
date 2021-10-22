from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .ioutils import mk_abstract_json


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
            mk_abstract_json(adapter.asdict())
            return item
