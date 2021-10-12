from requests_html import HTMLSession

session = HTMLSession()


def google_lat_lon(query: str):

    url = "https://www.google.com/maps/search/?api=1"
    params = {}
    params["query"] = query

    r = session.get(url, params=params)

    reg = "APP_INITIALIZATION_STATE=[[[{}]"
    res = r.html.search(reg)[0]
    lat = res.split(",")[2]
    lon = res.split(",")[1]

    return lat, lon


extraneous = "something whose latitude and longitude you would like to know, maybe "
relevant = "VUMC Internal Medicine"

query = extraneous + relevant

lat, lon = google_lat_lon(query)

print(
       "Hello. "
       "My name is Google. "
       "I am really good at guessing what you meant. "
      f"Your query was '{query}'. "
       "Here are the coordinates you probably wanted. "
      f"The latitude is {lat}, and the longitude is {lon}. "
       "Don't believe me? "
       "Here it is again, "
       "in a format you can paste into the search bar: \n"
      f"{lat}, {lon} \n"
       "Told ya. "
)
