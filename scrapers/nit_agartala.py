import requests
from bs4 import BeautifulSoup

def scrape_nit_agartala(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        status = "Closed"
        deadline = "31 March 2026 (Online) | 15 April 2026 (Hard Copy)"

        if "open" in text:
            status = "Open"

        return {
            "post": "Associate Professor / Professor",
            "eligibility": "Ph.D. in relevant discipline",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("NIT Agartala Error:", e)
        return None