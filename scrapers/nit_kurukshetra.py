import requests
from bs4 import BeautifulSoup


def scrape_nit_kurukshetra(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        status = "Open"
        deadline = "Not Mentioned"

        if "closed" in text:
            status = "Closed"

        if "last date" in text:
            deadline = "Check Official Advertisement"

        return {
            "post": "Assistant Professor / Associate Professor / Professor",
            "eligibility": "As per official advertisement",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("NIT Kurukshetra Error:", e)
        return None