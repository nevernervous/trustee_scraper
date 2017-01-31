import os
from datetime import datetime

import requests
from lxml import html as lxml_html

from myLogger import logger, get_main_dir
from constants import headers
from SL_Scraper.pdf_processor import process_pdf


def step1_scrape_sl():
    logger.info('Scraping from SouthLaw...')

    logger.info('\tFetching PDF Links...')
    url = 'http://www.southlaw.com/download/'
    r = requests.get(url, headers=headers)
    doc = lxml_html.fromstring(r.content)
    ahrefs = doc.xpath('//div[@class="wpb_wrapper"]/h4/a')
    pdflinks = ['http://www.southlaw.com' + ahref.get('href') for ahref in ahrefs]
    pdfnames = []
    for i, pdflink in enumerate(pdflinks):
        fname = pdflink[pdflink.rindex('/') + 1:]
        logger.info('\t%s/%s: Downloading %s' % (i + 1, len(pdflinks), fname))
        r = requests.get(pdflink, headers=headers)
        fpath = os.path.join(get_main_dir(), 'SL_Scraper', 'Files', 'temp', fname)
        pdfnames.append(fname)
        with open(fpath, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    for i, pdfname in enumerate(pdfnames):
        logger.info('\tProcessing %s/%s: %s' % (i + 1, len(pdfnames), pdfname))
        process_pdf(pdfname)
