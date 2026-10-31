import requests
from bs4 import BeautifulSoup


def scrape_iit_madras(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        status = "Open"
        deadline = "Rolling Advertisement"

        if "closed" in text:
            status = "Closed"

        return {
            "post": "Assistant Professor",
            "eligibility": "As per official advertisement",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("IIT Madras Error:", e)
        return None