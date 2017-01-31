from datetime import datetime

import requests
from lxml import html as lxml_html

from Trustee import models
from myLogger import logger
from constants import headers, KOZ


def step1_scrape_kmlaw():
    logger.info('Scraping from Kozney...')

    # Scrape Kozeny
    url = 'http://km-law.com/kmcis/sales.php?c=1'
    r = requests.get(url, headers=headers)
    doc = lxml_html.fromstring(r.content)
    trs = doc.xpath('//h2/following-sibling::table[./tr[@class="bidhead"]]/tr')
    for tr in trs:
        if 'Sale Date' in tr.text_content().strip():
            continue
        tds = tr.xpath('./td')
        file_num = tds[2].text_content().strip()
        site_state = tds[5].text_content().strip()

        propertyrecord = models.PropertyRecord.objects.get_or_create(
            trustee=KOZ, trustee_file_num=file_num, trustee_state=site_state)[0]
        sale_datetime = '%s %s' % (tds[0].text_content().strip(), tds[1].text_content().strip())
        propertyrecord.trustee_sale_datetime = datetime.strptime(sale_datetime, '%m/%d/%Y %I:%M %p')
        propertyrecord.trustee_address = tds[3].text_content().strip()
        propertyrecord.trustee_county = tds[4].text_content().strip()

        bid = tds[6].text_content().strip()
        propertyrecord.trustee_bid = None if bid == 'Not Available' else float(bid.replace('$', '').replace(',', '').strip())
        propertyrecord.save()
