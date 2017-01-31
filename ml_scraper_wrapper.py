import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PropertyScraper_Web.settings")
django.setup()

from ML_Scraper import scraper
import Zillow_Scraper
from constants import ML


def main():
    scraper.step1_scrape_ml()
    Zillow_Scraper.scrape_zillow(ML)


if __name__ == '__main__':
    main()
