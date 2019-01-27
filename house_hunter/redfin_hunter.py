# -*- coding: utf-8 -*-
"""

"""
import requests
import json
import warnings
from dataclasses import dataclass, InitVar

_SINGLE_HOME_BASE = 'https://www.redfin.com/stingray/api/home/details/belowTheFold?' \
                        'propertyId={propertyId}&accessLevel=1&listingId={listingId}'

_LOCATION_SEARCH_BASE = 'https://www.redfin.com/stingray/do/location-autocomplete?' \
                        'location={location}&start=0&count=10&v=2'

_LOCATION_TYPE_SWITCH = {
    6: 1,
    2: 6,
    3: 7
}


_LISTING_SEARCH_BASE = 'https://www.redfin.com/stingray/api/gis?al=1&v=8&status=9&' \
                       'region_id={region_id}&region_type={region_type}&num_homes=10000'

_REQUEST_HEADER = {
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


@dataclass()
class RedfinListing:
    listing_id: int
    property_id: int
    summary_dict: dict = None
    comprehensive_dict: dict = None
    do_full_retrieval: InitVar[bool] = False

    def __post_init__(self, do_full_retrieval):
        if self.listing_id is None or self.property_id is None:
            assert self.summary_dict is not None, \
                'If listing_id and property_id are omitted, a summary dictionary must be inclued!'
            if self.listing_id is None: self.listing_id = self.summary_dict.get('listingId')
            if self.property_id is None: self.property_id = self.summary_dict.get('propertyId')
        assert self.listing_id is not None, 'listing_id must be given'
        assert self.property_id is not None, 'property_id must be given'

        if do_full_retrieval:
            success = self.populate_details()
            if not success: warnings.warn('Retrieval of full details was requested but unsuccessful')

    @classmethod
    def from_summary(cls, summary_dict):
        listing_id = summary_dict.get('listingId')
        property_id = summary_dict.get('propertyId')
        return cls(listing_id=listing_id, property_id=property_id, summary_dict=summary_dict)

    @property
    def has_summary(self):
        return self.summary_dict is not None

    @property
    def has_full_listing(self):
        return self.comprehensive_dict is not None

    def populate_details(self):
        single_home_url = _SINGLE_HOME_BASE.format(propertyId=self.property_id, listingId=self.listing_id)
        response = requests.get(single_home_url, headers=_REQUEST_HEADER)
        if not response.ok: return False
        json_str = response.content.decode('utf-8').replace('{}&&', '')
        json_data = json.loads(json_str)
        if json_data['errorMessage'] != 'Success': return False
        self.comprehensive_dict = json_data['payload']
        return True


class RedfinListingSearch:

    @classmethod
    def do_search(cls, region_type, region_id, do_type_switch=True, **kwargs):
        if do_type_switch:
            region_type = _LOCATION_TYPE_SWITCH[region_type]
        url_temp = _LISTING_SEARCH_BASE.format(region_type=region_type, region_id=region_id)
        if len(kwargs) > 0:
            url_temp = url_temp + '&' + '&'.join([key + '=' + str(val) for key, val in kwargs.items()])
            print(url_temp)
        response = requests.get(url_temp, headers=_REQUEST_HEADER)
        if not response.ok:
            warnings.warn('Failed search results - Bad Response')
            return None
        response_content = response.content.decode('utf-8')
        json_str = response_content.replace('{}&&', '')
        json_data = json.loads(json_str)
        if json_data['errorMessage'] != 'Success':
            warnings.warn('Failed search results - Failure Message: {}'.format(json_data['errorMessage']))
            return None

        return [RedfinListing.from_summary(summary) for summary in json_data['payload']['homes']]

    @classmethod
    def do_search_by_id_str(cls, region_str):
        region_id = region_str.split('_')[-1]
        region_type = int(region_str.split('_')[0])
        return cls.do_search(region_type=region_type, region_id=region_id, do_type_switch=True)

    @classmethod
    def do_poly_search(cls, user_poly, **kwargs):
        url_temp = 'https://www.redfin.com/stingray/api/gis?al=1&v=8&status=9&num_homes=10000&user_poly=' + user_poly
        if len(kwargs) > 0:
            url_temp = url_temp + '&' + '&'.join([key + '=' + str(val) for key, val in kwargs.items()])
            print(url_temp)
        response = requests.get(url_temp, headers=_REQUEST_HEADER)
        if not response.ok:
            warnings.warn('Failed search results - Bad Response')
            return None
        response_content = response.content.decode('utf-8')
        json_str = response_content.replace('{}&&', '')
        json_data = json.loads(json_str)
        if json_data['errorMessage'] != 'Success':
            warnings.warn('Failed search results - Failure Message: {}'.format(json_data['errorMessage']))
            return None

        return [RedfinListing.from_summary(summary) for summary in json_data['payload']['homes']]

    @classmethod
    def parse_user_poly_from_url(cls, url: str) -> str:
        """
        Strip the user_poly parameter from a search URL originated from redfin.com

        :param url: URL string
        :return: user_poly string from url (or None if not found)
        """
        params = url.split('?')[-1]
        url_split = params.split('&')

        for param in url_split:
            if param.split('=')[0].lower() == 'user_poly':
                return param.split('=')[-1]
        return None


class RedfinLocationSearch:

    @classmethod
    def do_search(cls, search_term: str, is_addr: bool=False) -> list:
        """
        Search redfin for matching location names (or addresses)

        :param search_term: Search string
        :param is_addr: True if specifying an address rather than a location
        :return: list
        """
        location_url = _LOCATION_SEARCH_BASE.format(location=search_term)
        response = requests.get(location_url, headers=_REQUEST_HEADER)
        if not response.ok: return None
        json_str = response.content.decode('utf-8').replace('{}&&', '')
        json_data = json.loads(json_str)
        if json_data['errorMessage'] != 'Success': return None
        result_dict = {data['name']: data['rows'] for data in json_data['payload']['sections']}
        if is_addr:
            return result_dict.get('Addresses') or []
        return result_dict.get('Places') or []


class HouseHunt:
    pass
