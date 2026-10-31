import json
from datetime import datetime
from pathlib import Path

from scrapers.iit_bhilai import scrape_iit_bhilai
from scrapers.iit_bhu import scrape_iit_bhu
from scrapers.iit_bhubaneswar import scrape_iit_bhubaneswar
from scrapers.iit_delhi import scrape_iit_delhi
from scrapers.iit_dharwad import scrape_iit_dharwad
from scrapers.iit_gandhinagar import scrape_iit_gandhinagar
from scrapers.iit_goa import scrape_iit_goa
from scrapers.iit_hyderabad import scrape_iit_hyderabad
from scrapers.iit_indore import scrape_iit_indore
from scrapers.iit_jammu import scrape_iit_jammu
from scrapers.iit_jodhpur import scrape_iit_jodhpur
from scrapers.iit_kanpur import scrape_iit_kanpur
from scrapers.iit_kharagpur import scrape_iit_kharagpur
from scrapers.iit_madras import scrape_iit_madras
from scrapers.iit_mandi import scrape_iit_mandi
from scrapers.iit_palakkad import scrape_iit_palakkad
from scrapers.iit_patna import scrape_iit_patna
from scrapers.iit_roorkee import scrape_iit_roorkee
from scrapers.iit_ropar import scrape_iit_ropar
from scrapers.iit_tirupati import scrape_iit_tirupati
from scrapers.nit_agartala import scrape_nit_agartala
from scrapers.nit_calicut import scrape_nit_calicut
from scrapers.nit_durgapur import scrape_nit_durgapur
from scrapers.nit_hamirpur import scrape_nit_hamirpur
from scrapers.nit_jamshedpur import scrape_nit_jamshedpur
from scrapers.nit_kurukshetra import scrape_nit_kurukshetra
from scrapers.nit_patna import scrape_nit_patna
from scrapers.nit_raipur import scrape_nit_raipur
from scrapers.nit_rourkela import scrape_nit_rourkela
from scrapers.nit_silchar import scrape_nit_silchar
from scrapers.nit_srinagar import scrape_nit_srinagar
from scrapers.nit_surathkal import scrape_nit_surathkal
from scrapers.nit_trichy import scrape_nit_trichy
from scrapers.nit_warangal import scrape_nit_warangal

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data.json"
METADATA_PATH = BASE_DIR / "sync_metadata.json"

SCRAPERS = {
    "IIT Bhilai": scrape_iit_bhilai,
    "IIT BHU": scrape_iit_bhu,
    "IIT Bhubaneswar": scrape_iit_bhubaneswar,
    "IIT Delhi": scrape_iit_delhi,
    "IIT Dharwad": scrape_iit_dharwad,
    "IIT Gandhinagar": scrape_iit_gandhinagar,
    "IIT Goa": scrape_iit_goa,
    "IIT Hyderabad": scrape_iit_hyderabad,
    "IIT Indore": scrape_iit_indore,
    "IIT Jammu": scrape_iit_jammu,
    "IIT Jodhpur": scrape_iit_jodhpur,
    "IIT Kanpur": scrape_iit_kanpur,
    "IIT Kharagpur": scrape_iit_kharagpur,
    "IIT Madras": scrape_iit_madras,
    "IIT Mandi": scrape_iit_mandi,
    "IIT Palakkad": scrape_iit_palakkad,
    "IIT Patna": scrape_iit_patna,
    "IIT Roorkee": scrape_iit_roorkee,
    "IIT Ropar": scrape_iit_ropar,
    "IIT Tirupati": scrape_iit_tirupati,
    "NIT Agartala": scrape_nit_agartala,
    "NIT Calicut": scrape_nit_calicut,
    "NIT Durgapur": scrape_nit_durgapur,
    "NIT Hamirpur": scrape_nit_hamirpur,
    "NIT Jamshedpur": scrape_nit_jamshedpur,
    "NIT Kurukshetra": scrape_nit_kurukshetra,
    "NIT Patna": scrape_nit_patna,
    "NIT Raipur": scrape_nit_raipur,
    "NIT Rourkela": scrape_nit_rourkela,
    "NIT Silchar": scrape_nit_silchar,
    "NIT Srinagar": scrape_nit_srinagar,
    "NIT Surathkal": scrape_nit_surathkal,
    "NIT Tiruchirappalli": scrape_nit_trichy,
    "NIT Warangal": scrape_nit_warangal,
}


def _write_json(path, value):
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(value, file, indent=4, ensure_ascii=False)
            file.write("\n")
        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def update_recruitments():
    with DATA_PATH.open(encoding="utf-8") as file:
        recruitments = json.load(file)
    if not isinstance(recruitments, list):
        raise ValueError(f"{DATA_PATH} must contain a JSON array")

    updated = 0
    failed = 0
    print("Checking recruitment websites...\n")

    for job in recruitments:
        institute = job.get("institute", "Unknown institute")
        scraper = SCRAPERS.get(institute)
        if scraper is None:
            print(f"Skipping {institute}: no scraper is configured.")
            failed += 1
            continue

        print(f"Checking: {institute}")
        try:
            new_data = scraper(job["source_url"])
        except (KeyError, OSError, ValueError, TypeError) as error:
            print(f"{institute} scraper failed: {error}")
            failed += 1
            continue

        if not isinstance(new_data, dict) or not new_data:
            print(f"{institute} returned no update.")
            failed += 1
            continue

        job.update(new_data)
        updated += 1
        print("Updated successfully.")

    if updated:
        _write_json(DATA_PATH, recruitments)
        last_updated = datetime.now().astimezone().strftime("%d %B %Y, %I:%M %p %Z")
        _write_json(METADATA_PATH, {"last_updated": last_updated})
        print(f"\nUpdated {updated} of {len(recruitments)} records.")
        print(f"Last successful sync: {last_updated}")
    else:
        print("\nNo recruitment records were updated; existing data was preserved.")

    if failed:
        print(f"{failed} record(s) could not be refreshed.")

    return updated, failed


if __name__ == "__main__":
    update_recruitments()
