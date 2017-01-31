import requests

from myLogger import logger
from constants import google_maps_api_key, KOZ, CENT, ML, SL


def get_google_maps_data(propertyrecord):
    logger.info('\tFetching data from Google Maps...')

    if propertyrecord.trustee == KOZ:
        address = '%s, %s, %s' % (propertyrecord.trustee_address, propertyrecord.trustee_county, propertyrecord.trustee_state)
    elif propertyrecord.trustee == CENT:
        address = '%s, %s, MO' % (propertyrecord.trustee_address, propertyrecord.trustee_county)
    elif propertyrecord.trustee in [ML, SL]:
        address = '%s, %s, %s %s, USA' % (propertyrecord.trustee_address, propertyrecord.trustee_city, propertyrecord.trustee_state, propertyrecord.trustee_zipcode)
    else:
        propertyrecord.googlemaps_api_comments = 'Trustee Not Found'
        return False

    google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (address, google_maps_api_key)
    r = requests.get(google_url).json()
    if len(r['results']) == 0:
        propertyrecord.googlemaps_api_comments = r['status']
        return False

    formatted_address = r['results'][0]['formatted_address']
    propertyrecord.google_maps_address = formatted_address.split(',')[0].strip()

    for address_component in r['results'][0]['address_components']:
        if 'postal_code' in address_component['types']:
            propertyrecord.google_maps_zipcode = address_component['long_name']
            break
    if propertyrecord.google_maps_zipcode in [None, '']:
        propertyrecord.comments = 'ZipCode not found in Google Maps data'
        return False
    return True
