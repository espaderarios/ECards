import requests
import urllib.parse


def build_query(keywords):
    if not keywords:
        return ""
    return " ".join(keywords[:5]) + " explanation"


def search_wikipedia(query: str) -> str:
    if not query:
        return ""
    try:
        search_url = "https://en.wikipedia.org/w/rest.php/v1/search/page"
        params = {"q": query, "limit": 1}
        r = requests.get(search_url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        pages = data.get("pages", [])
        if not pages:
            return "No results found"
        title = pages[0]["title"]
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
        sr = requests.get(summary_url, timeout=10)
        sr.raise_for_status()
        return sr.json().get("extract", "No summary available")
    except Exception:
        return "Wikipedia lookup failed"
