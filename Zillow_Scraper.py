from datetime import datetime
import xml.etree.ElementTree as ET


import requests

from Trustee import models
import google_maps_scraper
from myLogger import logger
from constants import headers, zillow_api_keys
from utilities import get_proxy


def scrape_zillow(trustee):
    logger.info('Processing All Properties in Zillow for {}'.format(trustee))

    unp_propery_records_count = models.PropertyRecord.objects.filter(trustee=trustee, is_zillow_processed=False).count()
    if unp_propery_records_count == 0:
        return
    unp_propery_records = models.PropertyRecord.objects.filter(trustee=trustee, is_zillow_processed=False).all()

    for i, propertyrecord in enumerate(unp_propery_records):
        logger.info('\t%s: %s/%s: %s' % (
            propertyrecord.trustee, i + 1, unp_propery_records_count, propertyrecord.trustee_file_num))
        process_single_property_record_zillow(propertyrecord)
        # break


def process_single_property_record_zillow(propertyrecord):
    # Step1: Fetch from Google
    res = google_maps_scraper.get_google_maps_data(propertyrecord)
    propertyrecord.is_zillow_processed = True
    if res is False:
        propertyrecord.save()
        return

    # Step2: Fetch from GetDeepSearchResults API
    res = fetch_from_getdeepsearchresults_api(propertyrecord)
    if res is False:
        propertyrecord.is_zillow_processed = True
    propertyrecord.save()

    if propertyrecord.zpid is None:
        return

    # Step3: Fetch from GetUpdatedPropertyDetails API
    fetch_from_getupdatedpropertydetails_api(propertyrecord)
    propertyrecord.save()

    # Step4: Fetch from GetMonthlyPayments API (Mortgage)
    # fetch_from_getmonthlypayments_api(propertyrecord)
    # propertyrecord.save()


def zillow_requests_get(zillow_url):
    attempt_count = 0
    while True:
        attempt_count += 1
        logger.info('\t\tAttempt {}'.format(attempt_count))
        proxies = get_proxy()
        try:
            r = requests.get(zillow_url, headers=headers, proxies=proxies, timeout=60)
            parser = ET.XMLParser(encoding="utf-8")
            root = ET.fromstring(r.content.decode(), parser=parser)
            return_code = root.find('./message/code').text
            return root
        except (AttributeError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            # logger.exception(e)
            continue
        except ET.ParseError:
            # logger.error('Parse Error')
            # with open('temp.xml', 'w') as f:
            #     f.write(r.content.decode())
            continue


def fetch_from_getdeepsearchresults_api(propertyrecord):
    logger.info('\tFetching data from GetDeepSearchResults API...')
    zillow_url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id={}&address={}&citystatezip={}&rentzestimate=true'.format(
        zillow_api_keys[propertyrecord.trustee], propertyrecord.google_maps_address, propertyrecord.google_maps_zipcode
    )

    root = zillow_requests_get(zillow_url)
    propertyrecord.property1_return_code = int(root.find('./message/code').text)
    propertyrecord.property1_comments = root.find('./message/text').text.strip()
    logger.info('\t\t{}'.format(root.find('./message/text').text.strip()))
    if propertyrecord.property1_return_code not in [0, '0']:
        return False

    result = root.find('./response/results/result')
    propertyrecord.zpid = find_tag_value(result, 'zpid', int)

    propertyrecord.link_homedetails = find_tag_value(result, './links/homedetails')
    propertyrecord.link_chartdata = find_tag_value(result, './links/graphsanddata')
    propertyrecord.link_mapthishome = find_tag_value(result, './links/mapthishome')
    propertyrecord.link_similarsales = find_tag_value(result, './links/comparables')

    propertyrecord.street_address = find_tag_value(result, './address/street')
    propertyrecord.zipcode = find_tag_value(result, './address/zipcode')
    propertyrecord.city = find_tag_value(result, './address/city')
    propertyrecord.state = find_tag_value(result, './address/state')
    propertyrecord.latitude = find_tag_value(result, './address/latitude')
    propertyrecord.longitude = find_tag_value(result, './address/longitude')

    propertyrecord.fipscounty = find_tag_value(result, 'FIPScounty')
    propertyrecord.usecode = find_tag_value(result, 'useCode')
    propertyrecord.taxassessment_year = find_tag_value(result, 'taxAssessmentYear', int)
    propertyrecord.taxassessment_amount = find_tag_value(result, 'taxAssessment', float)
    propertyrecord.yearbuilt = find_tag_value(result, 'yearBuilt', int)
    propertyrecord.lotsize_sqft = find_tag_value(result, 'lotSizeSqFt', float)
    propertyrecord.finished_sqft = find_tag_value(result, 'finishedSqFt', float)
    propertyrecord.bathrooms = find_tag_value(result, 'bathrooms', float)
    propertyrecord.bedrooms = find_tag_value(result, 'bedrooms', float)
    propertyrecord.totalrooms = find_tag_value(result, 'totalRooms', float)
    lastsold_date = find_tag_value(result, 'lastSoldDate')
    propertyrecord.lastsold_date = datetime.strptime(lastsold_date, '%m/%d/%Y').date() if lastsold_date is not None else None
    propertyrecord.lastsold_price = find_tag_value(result, 'lastSoldPrice', float)

    propertyrecord.zestimate_amount = find_tag_value(result, './zestimate/amount', float)
    zestimate_lastupdated = find_tag_value(result, './zestimate/last-updated')
    propertyrecord.zestimate_lastupdated = datetime.strptime(zestimate_lastupdated, '%m/%d/%Y').date() if zestimate_lastupdated is not None else None
    propertyrecord.zestimate_30daychange = find_tag_value(result, './zestimate/valueChange', float)
    propertyrecord.zestimate_valuationrangelow = find_tag_value(result, './zestimate/valuationRange/low', float)
    propertyrecord.zestimate_valuationrangehigh = find_tag_value(result, './zestimate/valuationRange/high', float)
    propertyrecord.zestimate_percentile = find_tag_value(result, './zestimate/percentile', float)

    propertyrecord.rzestimate_amount = find_tag_value(result, './rentzestimate/amount', float)

    rzestimate_lastupdated = find_tag_value(result, './rentzestimate/last-updated')
    propertyrecord.rzestimate_lastupdated = datetime.strptime(rzestimate_lastupdated, '%m/%d/%Y').date() if rzestimate_lastupdated is not None else None
    propertyrecord.rzestimate_30daychange = find_tag_value(result, './rentzestimate/valueChange', float)
    propertyrecord.rzestimate_valuationrangelow = find_tag_value(result, './rentzestimate/valuationRange/low', float)
    propertyrecord.rzestimate_valuationrangehigh = find_tag_value(result, './rentzestimate/valuationRange/high', float)

    propertyrecord.localrealestate_overviewurl = find_tag_value(result, './localRealEstate/region/links/overview')
    propertyrecord.localrealestate_forsalebyownerurl = find_tag_value(result, './localRealEstate/region/links/forSaleByOwner')
    propertyrecord.localrealestate_forsalehomesurl = find_tag_value(result, './localRealEstate/region/links/forSale')

    if propertyrecord.zestimate_amount is not None:
        propertyrecord.is_mortgage_being_saved = True

    return True


def fetch_from_getupdatedpropertydetails_api(propertyrecord):
    logger.info('\tFetching data from GetUpdatedPropertyDetails API')
    zillow_url = 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id={}&zpid={}'.format(
        zillow_api_keys[propertyrecord.trustee], propertyrecord.zpid)

    root = zillow_requests_get(zillow_url)

    propertyrecord.property2_return_code = root.find('./message/code').text
    propertyrecord.property2_comments = root.find('./message/text').text.strip()
    logger.info('\t\t{}'.format(root.find('./message/text').text.strip()))
    if propertyrecord.property2_return_code not in [0, '0']:
        return

    response = root.find('./response')
    propertyrecord.pageviewcount_currentmonth = find_tag_value(response, './pageViewCount/currentMonth', int)
    propertyrecord.pageviewcount_total = find_tag_value(response, './pageViewCount/total', int)

    propertyrecord.posting_status = find_tag_value(response, './posting/status')
    propertyrecord.posting_agentname = find_tag_value(response, './posting/agentName')
    propertyrecord.posting_agentprofileurl = find_tag_value(response, './posting/agentProfileUrl')
    propertyrecord.posting_brokerage = find_tag_value(response, './posting/brokerage')
    propertyrecord.posting_type = find_tag_value(response, './posting/type')
    posting_lastupdateddate = find_tag_value(response, './posting/lastUpdatedDate')
    propertyrecord.posting_lastupdateddate = datetime.strptime(posting_lastupdateddate,
                                                               '%Y-%m-%d %H:%M:%S.%f') if posting_lastupdateddate is not None else None
    propertyrecord.posting_externalurl = find_tag_value(response, './posting/externalUrl')
    propertyrecord.posting_mls = find_tag_value(response, './posting/mls')

    propertyrecord.price = find_tag_value(response, './price', float)

    propertyrecord.photogallery_url = find_tag_value(response, './links/photoGallery')
    for i, imageurl in enumerate(response.findall('./images/image/url')):
        setattr(propertyrecord, 'image_url{}'.format(i + 1), imageurl.text.strip())

    propertyrecord.year_updated = find_tag_value(response, './editedFacts/yearUpdated', int)
    propertyrecord.num_floors = find_tag_value(response, './editedFacts/numFloors', int)
    propertyrecord.basement = find_tag_value(response, './editedFacts/basement')
    propertyrecord.roof = find_tag_value(response, './editedFacts/roof')
    propertyrecord.view = find_tag_value(response, './editedFacts/view')
    propertyrecord.parking_type = find_tag_value(response, './editedFacts/parkingType')
    propertyrecord.heating_sources = find_tag_value(response, './editedFacts/heatingSources')
    propertyrecord.heating_system = find_tag_value(response, './editedFacts/heatingSystem')
    propertyrecord.appliances = find_tag_value(response, './editedFacts/appliances')
    propertyrecord.floor_covering = find_tag_value(response, './editedFacts/floorCovering')
    propertyrecord.rooms_desc = find_tag_value(response, './editedFacts/rooms')
    propertyrecord.covered_parking_spaces = find_tag_value(response, './editedFacts/coveredParkingSpaces', int)
    propertyrecord.cooling_system = find_tag_value(response, './editedFacts/coolingSystem')
    propertyrecord.architecture = find_tag_value(response, './editedFacts/architecture')
    propertyrecord.floor_number = find_tag_value(response, './editedFacts/floorNumber', int)
    propertyrecord.num_units = find_tag_value(response, './editedFacts/numUnits', int)

    propertyrecord.home_description = find_tag_value(response, './homeDescription')
    propertyrecord.what_owner_loves = find_tag_value(response, './whatOwnerLoves')
    propertyrecord.neighborhood = find_tag_value(response, './neighborhood')
    propertyrecord.school_district = find_tag_value(response, './schoolDistrict')
    propertyrecord.elementary_school = find_tag_value(response, './elementarySchool')
    propertyrecord.middle_school = find_tag_value(response, './middleSchool')
    propertyrecord.high_school = find_tag_value(response, './highSchool')


def fetch_from_getmonthlypayments_api(propertyrecord):
    logger.info('\tFetching data from GetMonthlyPayments API')
    if propertyrecord.zestimate_amount is None:
        propertyrecord.mortgage_comments = 'Zestimate Amount Not Available'
        return
    if propertyrecord.zipcode is None:
        propertyrecord.mortgage_comments = 'Zipcode Not Available'
        return
    zillow_url = 'http://www.zillow.com/webservice/GetMonthlyPayments.htm?zws-id={}&price={}&zip={}'.format(
        zillow_api_keys[propertyrecord.trustee], int(propertyrecord.zestimate_amount), propertyrecord.zipcode)

    root = zillow_requests_get(zillow_url)

    propertyrecord.mortgage_return_code = root.find('./message/code').text
    propertyrecord.mortgage_comments = root.find('./message/text').text.strip()
    logger.info('\t\t{}'.format(root.find('./message/text').text.strip()))
    if propertyrecord.mortgage_return_code not in [0, '0']:
        return
    response = root.find('./response')
    propertyrecord.mortgage_30yearfixed_rate = find_tag_value(response, './payment[@loanType="thirtyYearFixed"]/rate', float)
    propertyrecord.mortgage_30yearfixed_pi = find_tag_value(response, './payment[@loanType="thirtyYearFixed"]/monthlyPrincipalAndInterest', float)
    propertyrecord.mortgage_15yearfixed_rate = find_tag_value(response, './payment[@loanType="fifteenYearFixed"]/rate', float)
    propertyrecord.mortgage_15yearfixed_pi = find_tag_value(response, './payment[@loanType="fifteenYearFixed"]/monthlyPrincipalAndInterest', float)
    propertyrecord.mortgage_51arm_rate = find_tag_value(response, './payment[@loanType="fiveOneARM"]/rate', float)
    propertyrecord.mortgage_51arm_pi = find_tag_value(response, './payment[@loanType="fiveOneARM"]/monthlyPrincipalAndInterest', float)
    propertyrecord.mortgage_downpayment = find_tag_value(response, './downPayment', float)
    propertyrecord.mortgage_monthlypropertytaxes = find_tag_value(response, './monthlyPropertyTaxes', float)
    propertyrecord.mortgage_monthlyinsurance = find_tag_value(response, './monthlyHazardInsurance', float)
    propertyrecord.is_mortgage_being_saved = True


def find_tag_value(response, xpath, returntype=None):
    try:
        result = response.find(xpath).text.strip()
        if returntype is None:
            return result
        else:
            return returntype(result)
    except AttributeError:
        return None
    except ValueError:
        return None
