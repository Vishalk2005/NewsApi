import requests
import urllib3
import json
import time

from newsdataapi import NewsDataApiClient

# Disable SSL verification warnings
urllib3.disable_warnings()
old_get = requests.get
requests.get = lambda *args, **kwargs: old_get(*args, verify=False, **kwargs)

# API setup
API_KEY = "pub_1a217eee8fde4e1db8e0ac851a477062"
KEYWORDS = ["breach", "ransomware", "acquisition", "lawsuit", "cyberattack"]
api = NewsDataApiClient(apikey=API_KEY)

def fetch_vendor_news(vendor):
    try:
        # Smart query: quote vendor, add keywords only if within 100-char limit
        query_base = f'"{vendor}"'
        extended_query = f'{query_base} {" OR ".join(KEYWORDS)}'
        query = extended_query if len(extended_query) <= 100 else query_base

        response = api.latest_api(q=query, country="us", language="en")
        all_results = response.get("results", [])

        # Filter: vendor name must appear in title or description
        filtered = [
            article for article in all_results
            if vendor.lower() in (article.get("title") or "").lower()
            or vendor.lower() in (article.get("description") or "").lower()
        ]
        return filtered

    except Exception as e:
        print(f"[!] Error for {vendor}: {e}")
        return []

def main():
    print("[*] Reading vendors.txt...")
    with open("vendors.txt") as f:
        vendors = list(set([line.strip() for line in f if line.strip()]))  # De-duped

    print(f"[*] Loaded {len(vendors)} unique vendors.")

    all_news = []

    for vendor in vendors:
        print(f"\n🔍 Fetching news for: {vendor}")
        articles = fetch_vendor_news(vendor)
        print(f"[~] Got {len(articles)} articles for {vendor}")
        for article in articles:
            print(f"- {article.get('title', 'No Title')}")
        all_news.append({"vendor": vendor, "articles": articles})
        time.sleep(2.5)  # API rate limit buffer

    # Save results
    with open("vendor_news.json", "w") as out:
        json.dump(all_news, out, indent=2)

    print("\n✅ Done. Results saved to vendor_news.json")

if __name__ == "__main__":
    main()
