import json
import requests
import warnings
from dataclasses import dataclass, InitVar

from house_hunter.house import House
from house_hunter.redfin.const import SINGLE_HOME_SEARCH_URL_BASE, REQUEST_HEADER


@dataclass()
class RedfinListing:
    listing_id: int
    property_id: int
    summary_dict: dict = None
    comprehensive_dict: dict = None
    do_full_retrieval: InitVar[bool] = False
    house: House = None

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
        single_home_url = SINGLE_HOME_SEARCH_URL_BASE.format(propertyId=self.property_id, listingId=self.listing_id)
        response = requests.get(single_home_url, headers=REQUEST_HEADER)
        if not response.ok: return False
        json_str = response.content.decode('utf-8').replace('{}&&', '')
        json_data = json.loads(json_str)
        if json_data['errorMessage'] != 'Success': return False
        self.comprehensive_dict = json_data['payload']
        self._create_house_from_dict()
        return True

    def _create_house_from_dict(self):
        self.house = None


        pass
