#
SINGLE_HOME_SEARCH_URL_BASE = 'https://www.redfin.com/stingray/api/home/details/belowTheFold?' \
                              'propertyId={propertyId}&accessLevel=1&listingId={listingId}'

REGION_NAME_SEARCH_BASE = 'https://www.redfin.com/stingray/do/location-autocomplete?' \
                          'location={location}&start=0&count=10&v=2'
REGION_TYPE_DESCRIPTOR = {
    2: 'CITY',
    4: 'ZIPCODE',
    6: 'NEIGHBORHOOD'
}

LISTING_SEARCH_BASE = 'https://www.redfin.com/stingray/api/gis?al=1&v=8&status=9&' \
                      'region_id={region_id}&region_type={region_type}&num_homes=10000'
LISTING_SEARCH_BASE = 'https://www.redfin.com/stingray/api/gis?al=1&v=8&' \
                      'region_id={region_id}&region_type={region_type}&num_homes=10000'
REQUEST_HEADER = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':
        'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Language':
        'en-US,en;q=0.8',
    'Connection':
        'keep-alive'
}
