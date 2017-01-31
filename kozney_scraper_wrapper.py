import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PropertyScraper_Web.settings")
django.setup()

from Kozney_Scraper import scraper
import Zillow_Scraper
from constants import KOZ


def main():
    scraper.step1_scrape_kmlaw()
    Zillow_Scraper.scrape_zillow(KOZ)


if __name__ == '__main__':
    main()
