import json
import requests
from typing import Tuple

from house_hunter.redfin.const import REGION_NAME_SEARCH_BASE, REQUEST_HEADER

# Constant dictionary to translate the number in the region "id" string to the correct region id number
_REGION_ID_STR_TO_REGION_TYPE_INT = {
    "6": 1,
    "2": 6,
    "3": 7,
    "4": 2
}

def get_region_type_and_id_from_id_string(id_string: str) -> Tuple[int, int]:
    """
    Return a valid region_type and region_id from the "id" in a region search string like "#_#####"

    :param id_string: id string gathered from a region dictionary "id" key
    :return: region_id, region_type
    """
    id_str_num, region_id_str = id_string.split('_')
    region_id = int(region_id_str)
    region_type = _REGION_ID_STR_TO_REGION_TYPE_INT.get(id_str_num)
    if region_type is None:
        raise ValueError(f'Unable to find valid region type number for region string "{id_string}"')
    return region_id, region_type


def find_redfin_region_by_search_string(search_string: str, is_addr: bool=False) -> list:
    """
            Search redfin for matching location names (or addresses)

            :param search_term: Search string
            :param is_addr: True if specifying an address rather than a location
            :return: list
            """
    location_url = REGION_NAME_SEARCH_BASE.format(location=search_string)
    response = requests.get(location_url, headers=REQUEST_HEADER)
    if not response.ok: return None
    json_str = response.content.decode('utf-8').replace('{}&&', '')
    json_data = json.loads(json_str)
    if json_data['errorMessage'] != 'Success': return None
    result_dict = {data['name']: data['rows'] for data in json_data['payload']['sections']}
    if is_addr:
        return result_dict.get('Addresses') or []
    return result_dict.get('Places') or []


class RedfinLocationSearch:

    @classmethod
    def do_search(cls, search_term: str, is_addr: bool=False) -> list:
        """
        Search redfin for matching location names (or addresses)

        :param search_term: Search string
        :param is_addr: True if specifying an address rather than a location
        :return: list
        """
        location_url = REGION_NAME_SEARCH_BASE.format(location=search_term)
        response = requests.get(location_url, headers=REQUEST_HEADER)
        if not response.ok: return None
        json_str = response.content.decode('utf-8').replace('{}&&', '')
        json_data = json.loads(json_str)
        if json_data['errorMessage'] != 'Success': return None
        result_dict = {data['name']: data['rows'] for data in json_data['payload']['sections']}
        if is_addr:
            return result_dict.get('Addresses') or []
        return result_dict.get('Places') or []
