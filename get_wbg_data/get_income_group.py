import requests

def get_incomegroup_dicts() -> list[dict]:
    url = "https://wbhx.vercel.app/wb/wbhx.json?_shape=array"
    res = requests.get(url=url)
    dicts = res.json()

    return dicts

def get_incomegroup(dicts: list[dict], country_code: str, year: int) -> str:

    row = next(item for item in dicts if item["Country Code"] == country_code)
    income_group = row[f"{year}"]

    return income_group

# income_group_dicts = get_incomegroup_dicts()
# income_group = get_incomegroup(income_group_dicts, "USA", 1997)
# print(income_group)
