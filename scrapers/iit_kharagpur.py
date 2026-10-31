import requests
from bs4 import BeautifulSoup


def scrape_iit_kharagpur(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        status = "Open"
        deadline = "31 December 2026"

        if "closed" in text:
            status = "Closed"

        if "rolling" in text:
            deadline = "Rolling Advertisement"

        return {
            "post": "Assistant Professor / Associate Professor / Professor",
            "eligibility": "Ph.D. in relevant discipline",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("IIT Kharagpur Error:", e)
        return None