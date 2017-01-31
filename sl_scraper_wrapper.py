import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PropertyScraper_Web.settings")
django.setup()

from SL_Scraper import scraper
import Zillow_Scraper
from constants import SL


def main():
    scraper.step1_scrape_sl()
    Zillow_Scraper.scrape_zillow(SL)


if __name__ == '__main__':
    main()
