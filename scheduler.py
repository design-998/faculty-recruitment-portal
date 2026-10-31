import logging
import time

import schedule

from scraper import update_recruitments

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def scheduled_refresh():
    logging.info("Starting the daily recruitment refresh.")
    try:
        updated, failed = update_recruitments()
    except Exception:
        logging.exception("The scheduled recruitment refresh failed.")
        return
    logging.info(
        "Daily recruitment refresh finished: %s updated, %s not refreshed.",
        updated,
        failed,
    )


def main():
    schedule.every().day.at("02:00").do(scheduled_refresh)
    logging.info(
        "Recruitment refresh scheduled for 02:00 local time. "
        "Keep this process running for the schedule to execute."
    )
    while True:
        schedule.run_pending()
        time.sleep(20)


if __name__ == "__main__":
    main()
