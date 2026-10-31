import requests
from bs4 import BeautifulSoup


def scrape_iit_roorkee(url):
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
        deadline = "Rolling Advertisement"

        if "closed" in text:
            status = "Closed"

        return {
            "post": "Assistant Professor",
            "eligibility": "Ph.D. in relevant discipline",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("IIT Roorkee Error:", e)
        return None