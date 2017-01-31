import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PropertyScraper_Web.settings")
django.setup()

from Centre_Scraper import scraper
import Zillow_Scraper
from constants import CENT


def main():
    scraper.step1_scrape_centre()
    # Zillow_Scraper.scrape_zillow(CENT)


if __name__ == '__main__':
    main()
