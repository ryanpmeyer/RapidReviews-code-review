import requests
from tqdm import tqdm
import json

ORCID_access_token = r'763f4fad-556a-4219-80e0-af506da2fc39'
ORCID_refresh_token = r'1ff1a22b-5e38-422c-939b-45d3f5e58802'

def search_ORCID(name):
    """ Searches ORCID api for name, returns first result of expanded search """
    search_response = requests.get(
        "https://pub.orcid.org/v3.0/expanded-search/?q=" + str(name),
        headers = {
            'Authorization type and Access token': 'Bearer {}'.format(ORCID_access_token),
            'Content-type': 'application/vnd.orcid+json'
        }
    )
    if search_response:
        return search_response['expanded-result'][0]
    return None


with open('orcid_data.json','w') as outfile:
    results = {}
    with open("COVIDScholar_snapshot.json", 'r', encoding = "utf8") as paper_data:
        for line in tqdm(paper_data, total = 192442, position=0, leave=True):
            obj = json.loads(line)
            authors = obj['authors']
            for author in authors:
                try:
                    name = author['name']
                    if not name:
                        name = author['first_name'] + ' ' + author['last_name']
                    results[name] = search_ORCID(name)
                except:
                    # no name found in json
                    continue
    json.dump(results, outfile)