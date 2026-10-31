import requests
from bs4 import BeautifulSoup

def scrape_nit_trichy(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        status = "Closed"
        deadline = "06 April 2026, 5:30 PM IST (Online) | 16 April 2026, 5:30 PM IST (Hard Copy)"

        if "open" in text:
            status = "Open"

        return {
            "post": "Assistant Professor / Associate Professor / Professor",
            "eligibility": "Ph.D. in relevant discipline",
            "deadline": deadline,
            "status": status
        }

    except Exception as e:
        print("NIT Trichy Error:", e)
        return None