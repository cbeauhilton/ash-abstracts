import re


def remove_intr_by(string: str) -> str:
    # clean_str = re.sub("(.Intr\. by .*?)", "", string)
    clean_str = re.sub("\(Intr\..*?\)", "", string)
    return clean_str


clean = remove_intr_by("So and so is great, (pants by a fancy guy) whom we love")
print(clean)
