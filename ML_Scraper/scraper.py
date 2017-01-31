from datetime import datetime

import requests
from lxml import html as lxml_html

from Trustee import models
from myLogger import logger
from constants import headers, ML


def step1_scrape_ml():
    logger.info('Scraping from MartinLeigh...')

    # Scrape ML
    url = 'http://martinleigh.com/foreclosures.php'
    r = requests.get(url, headers=headers)
    doc = lxml_html.fromstring(r.content)
    trs = doc.xpath('//div[@id="foreclosures"]/table/tbody/tr')
    for tr in trs:
        tds = tr.xpath('./td')
        file_num = tds[3].text_content().strip()

        propertyrecord = models.PropertyRecord.objects.get_or_create(
            trustee=ML, trustee_file_num=file_num)[0]

        sale_time = '10:00:00' if tds[1].text_content().strip() == 'Array' else tds[1].text_content().strip()
        sale_datetime = '%s %s' % (tds[0].text_content().strip(), sale_time)
        propertyrecord.trustee_sale_datetime = datetime.strptime(sale_datetime, '%Y-%m-%d %H:%M:%S')

        propertyrecord.trustee_address = tds[4].text_content().strip()
        propertyrecord.trustee_city = tds[5].text_content().strip()
        propertyrecord.trustee_county = tds[6].text_content().strip()
        propertyrecord.trustee_state = tds[7].text_content().strip()
        propertyrecord.trustee_zipcode = tds[8].text_content().strip()

        bid = tds[9].text_content().strip().replace('$', '').replace(',', '').strip()
        propertyrecord.trustee_bid = None if bid == '' or bid == '0.00' else round(float(bid), 2)
        propertyrecord.save()
