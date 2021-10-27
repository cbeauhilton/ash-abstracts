import iso3166
import requests
import reverse_geocode


def get_country_offline(lat: float, lon: float) -> str:

    coordinates = [(lat, lon)]
    country = reverse_geocode.search(coordinates)[0]

    return country["country_code"]


def get_country_code_a3(country: str) -> str:
    """
    `country` could be a string with the full name,
    or the 2-letter, 3-letter, or numeric country code
    """
    return iso3166.countries.get(country).alpha3


def get_incomegroup_dicts() -> list[dict]:
    url = "https://wbhx.vercel.app/wb/wbhx.json?_shape=array"
    res = requests.get(url=url)
    dicts = res.json()

    return dicts


def get_incomegroup(dicts: list[dict], country_code: str, year: int) -> str:
    """
    country_code should be ISO3
    """

    row = next(item for item in dicts if item["Country Code"] == country_code)
    income_group = row[f"{year}"]

    return income_group


# income_group_dicts = get_incomegroup_dicts()

# lat = -26.16248995
# lon = 28.07402465
# country = get_country_offline(lat, lon)
# country_code = get_country_code_a3(country)
# income_group = get_incomegroup(income_group_dicts, country_code, 1997)

# print(country_code)
# print(income_group)
