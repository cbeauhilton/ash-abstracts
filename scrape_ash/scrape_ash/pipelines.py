from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .ioutils import mk_abstract_json

import json
from pathlib import Path
from urllib.parse import quote_plus, urlparse

DOI_JSON_PATH = "data/doi_json"

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


def doi_json_fname(doi_link: str):
    url_path = urlparse(doi_link).path
    # remove leading slash if it exists
    if url_path.startswith("/"):
        url_path = url_path[1:]
    fname = quote_plus(url_path)
    return fname

class JsonWriterPipeline:

    def __init__(self, p: str):
        self.p = DOI_JSON_PATH
        Path(p).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item.asdict())
        fname = doi_json_fname(doi_link=item_dict["doi"])
        with open(f"{self.p}/{fname}.json", "w") as f:
            json.dump(item_dict, f, indent=4)
        return item
