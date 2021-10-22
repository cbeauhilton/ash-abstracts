import requests

def get_unscraped():
    url = 'https://ash-abstracts.vercel.app/abstracts/abstracts.json?_sort=doi&is_scraped__exact=0&_shape=array'
    resp = requests.get(url=url)
    l = resp.json() 
    doi_list = [d['doi'] for d in l]

    return doi_list

doi_list = get_unscraped()

print(doi_list)
print(len(doi_list))
