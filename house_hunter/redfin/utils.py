import json
import requests

from house_hunter.redfin.const import REGION_NAME_SEARCH_BASE, REQUEST_HEADER


def _get_region_type_from_id_string(id_string: str):
    """
    Return a REGION_TYPE

    :param id_string:
    :return:
    """
    initial_num = id_string.split('_')[0]


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
