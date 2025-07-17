import requests
import urllib3

urllib3.disable_warnings()

# Override `requests.get` to disable SSL verification
old_get = requests.get
requests.get = lambda *args, **kwargs: old_get(*args, verify=False, **kwargs)

from newsdataapi import NewsDataApiClient

api = NewsDataApiClient(apikey="pub_1a217eee8fde4e1db8e0ac851a477062")

response = api.latest_api(q="pizza", max_result=5, country="us", language="en")

for article in response.get("results", []):
    print(f"- {article['title']}")
