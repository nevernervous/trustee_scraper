import subprocess
import os
from datetime import datetime
from copy import deepcopy

from lxml import html as lxml_html

from Trustee import models
from myLogger import logger, get_main_dir
from constants import SL


def process_pdf(pdf_fname):
    # logger.info('\tProcessing PDF %s' % pdf_fname)
    step1_convert_pdf_to_html(pdf_fname)
    step2_parse_html(pdf_fname)


def step1_convert_pdf_to_html(pdf_fname):
    logger.info('\t\tConverting to html...')

    pdf_fpath = os.path.join(get_main_dir(), 'SL_Scraper', 'Files', 'temp', pdf_fname)
    dest_dir = os.path.join(get_main_dir(), 'SL_Scraper', 'Files', 'temp')
    html_fname = pdf_fname.replace('.pdf', '.html')
    fnull = open(os.devnull, 'w')

    # pdf2html_exe = os.path.join(get_main_dir(), 'Resources', 'pdf2html', 'pdf2htmlEX.exe')
    # subprocess.call([pdf2html_exe, '--dest-dir', dest_dir, pdf_fpath, html_fname], stdout=fnull, stderr=subprocess.STDOUT)

    subprocess.call(['pdf2htmlEX', '--dest-dir', dest_dir, pdf_fpath, html_fname], stdout=fnull, stderr=subprocess.STDOUT)


def step2_parse_html(pdf_fname):
    logger.info('\t\tParsing Data...')

    state = pdf_fname[pdf_fname.rindex('_') + 1:pdf_fname.rindex('.')]

    # Scrape Data
    html_fpath = os.path.join(get_main_dir(), 'SL_Scraper', 'Files', 'temp', pdf_fname.replace('.pdf', '.html'))
    with open(html_fpath, 'r') as f:
        doc = lxml_html.fromstring(f.read())
    div_pfs = doc.xpath('//div[contains(@id, "pf")]')

    current_county = None
    for div_pf in div_pfs:
        # Find X coordinates
        x_address = div_pf.xpath('.//div[contains(@class, "c x") and .="Property Address"]')[0].get('class').split()[1]
        x_city = div_pf.xpath('.//div[contains(@class, "c x") and .="Property City"]')[0].get('class').split()[1]
        x_zip = div_pf.xpath('.//div[contains(@class, "c x") and .="Property Zip"]')[0].get('class').split()[1]
        x_saledate = div_pf.xpath('.//div[contains(@class, "c x") and .="Sale Date"]')[0].get('class').split()[1]
        x_saletime = div_pf.xpath('.//div[contains(@class, "c x") and .="Sale Time"]')[0].get('class').split()[1]
        x_ctddatetime = div_pf.xpath('.//div[contains(@class, "c x") and .="Continued Date/Time"]')[0].get('class').split()[1]
        x_bid = div_pf.xpath('.//div[contains(@class, "c x") and .="Opening Bid"]')[0].get('class').split()[1]
        x_filenum = div_pf.xpath('.//div[contains(@class, "c x") and .="Firm File#"]')[0].get('class').split()[1]

        div = div_pf.xpath('./div/div')[0]
        is_page_break = False
        while True:
            if is_page_break is True or 'Foreclosure Sales Report' in div.text_content() or 'Information Reported' in div.text_content():
                break
            if 'x1 ' in div.get('class'):
                current_county = div.text_content().strip()
                try:
                    div = div.xpath('./following-sibling::div[contains(@class, "%s ")]' % x_address)[0]
                    continue
                except IndexError:
                    break
            elif '%s ' % x_address in div.get('class'):
                trustee_city = trustee_zipcode = trustee_sale_datetime = trustee_bid = trustee_continued_datetime = None
                trustee_address = div.text_content().strip()
                while True:
                    div = div.xpath('./following-sibling::div')[0]
                    if '%s ' % x_address in div.get('class'):
                        break
                    elif 'x1 ' in div.get('class'):
                        break
                    elif 'Foreclosure Sales Report' in div.text_content() or 'Information Reported' in div.text_content():
                        is_page_break = True
                        break
                    elif '%s ' % x_city in div.get('class'):
                        trustee_city = div.text_content().strip()
                    elif '%s ' % x_zip in div.get('class'):
                        trustee_zipcode = div.text_content().strip()
                    elif '%s ' % x_saledate in div.get('class'):
                        trustee_sale_datetime = datetime.strptime(div.text_content().strip(), '%m/%d/%Y')
                    elif '%s ' % x_saletime in div.get('class'):
                        temp_datetime = datetime.strptime(div.text_content().strip(), '%I:%M %p')
                        trustee_sale_datetime = trustee_sale_datetime.replace(hour=temp_datetime.hour, minute=temp_datetime.minute)
                    elif '%s ' % x_bid in div.get('class'):
                        bid = div.text_content().replace('$', '').replace(',', '').strip()
                        trustee_bid = None if bid == 'N/A' else bid
                    elif '%s ' % x_filenum in div.get('class'):
                        trustee_file_num = div.text_content().strip()
                    elif '%s ' % x_ctddatetime in div.get('class'):
                        trustee_continued_datetime = datetime.strptime(div.text_content().strip(), '%m/%d/%Y %I:%M %p')

                propertyrecord = models.PropertyRecord.objects.get_or_create(trustee=SL,
                                                                             trustee_file_num=trustee_file_num,
                                                                             trustee_state=state)[0]
                propertyrecord.trustee_county = current_county
                propertyrecord.trustee_city = trustee_city
                propertyrecord.trustee_address = trustee_address
                propertyrecord.trustee_zipcode = trustee_zipcode
                propertyrecord.trustee_sale_datetime = trustee_sale_datetime
                propertyrecord.trustee_bid = float(trustee_bid) if trustee_bid is not None else None
                propertyrecord.trustee_continued_datetime = trustee_continued_datetime
                propertyrecord.save()
