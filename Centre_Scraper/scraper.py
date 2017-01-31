from datetime import datetime

import requests
from lxml import html as lxml_html

from Trustee import models
from myLogger import logger
from constants import headers, CENT


def step1_scrape_centre():
    logger.info('Scraping from Centre...')

    # Scrape Centre
    url = 'http://www.centretrustee.com/listproperties.asp'
    r = requests.get(url, headers=headers)
    doc = lxml_html.fromstring(r.content)
    trs = doc.xpath('//tr[./td[.="Sale Date"]]/following-sibling::tr')
    for tr in trs:
        tds = tr.xpath('./td')
        file_num = tds[3].text_content().strip()

        propertyrecord = models.PropertyRecord.objects.get_or_create(
            trustee=CENT, trustee_file_num=file_num)[0]

        sale_datetime = '%s %s' % (tds[0].text_content().strip(), tds[1].text_content().strip())
        sale_datetime = sale_datetime.encode('ascii', 'ignore')
        propertyrecord.trustee_sale_datetime = datetime.strptime(sale_datetime, '%B%d,%Y %I:%M%p')
        propertyrecord.trustee_address = tds[4].text_content().strip()
        propertyrecord.trustee_county = tds[2].text_content().strip()

        bid = tds[5].text_content().strip()
        propertyrecord.trustee_bid = None if bid == '' else float(bid.replace('$', '').replace(',', '').strip())
        propertyrecord.save()

