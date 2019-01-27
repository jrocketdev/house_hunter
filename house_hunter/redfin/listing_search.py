import json
import requests
import warnings

from house_hunter.redfin.const import _LOCATION_TYPE_SWITCH, LISTING_SEARCH_BASE, REQUEST_HEADER
from house_hunter.redfin.listing import RedfinListing


class RedfinListingSearch:

    @classmethod
    def do_search(cls, region_type, region_id, do_type_switch=True, **kwargs):
        if do_type_switch:
            region_type = _LOCATION_TYPE_SWITCH[region_type]
        url_temp = LISTING_SEARCH_BASE.format(region_type=region_type, region_id=region_id)
        if len(kwargs) > 0:
            url_temp = url_temp + '&' + '&'.join([key + '=' + str(val) for key, val in kwargs.items()])
            print(url_temp)
        response = requests.get(url_temp, headers=REQUEST_HEADER)
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
        """
        Search redfin with a given user_poly argument (from stingray api)

        :param user_poly: string the describes the poly outline (from Redfin)
        :param kwargs:
        :return:
        """
        url_temp = 'https://www.redfin.com/stingray/api/gis?al=1&v=8&status=9&num_homes=10000&user_poly=' + user_poly
        if len(kwargs) > 0:
            url_temp = url_temp + '&' + '&'.join([key + '=' + str(val) for key, val in kwargs.items()])
            print(url_temp)
        response = requests.get(url_temp, headers=REQUEST_HEADER)
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
