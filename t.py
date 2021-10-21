import os

def get_start_url_page():
    start_url_page = os.getenv("START_URL_PAGE_NUM")

    if start_url_page:
        start_url_page = int(start_url_page)
    else:
        start_url_page = 1

    return start_url_page

start_url_page = get_start_url_page()
print(f"page number: {start_url_page}")
print(start_url_page*4)

