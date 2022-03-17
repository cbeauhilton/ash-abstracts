from requests_html import HTMLSession

session = HTMLSession()

def google_lat_lon(query: str):

    """
    Usage:

        first_author_affiliation = "University of Utrecht, Hematology"

        lat, lon = google_lat_lon(first_author_affiliation)

        d = {}
        d["first_author_latitude"]  = lat
        d["first_author_longitude"] = lon

    """

    url = "https://www.google.com/maps/search/?api=1"
    params = {}
    params["query"] = query

    r = session.get(url, params=params)

    reg = "APP_INITIALIZATION_STATE=[[[{}]"
    res = r.html.search(reg)[0]
    lat = res.split(",")[2]
    lon = res.split(",")[1]

    return lat, lon
