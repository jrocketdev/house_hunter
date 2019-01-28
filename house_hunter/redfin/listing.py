import json
import requests
import warnings
from dataclasses import dataclass, InitVar
import logging
import numpy as np

from house_hunter.house import House, Bedroom, Bathroom
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
        self._logger = logging.getLogger(self.__class__.__name__)
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
        elif self.summary_dict is not None:
            self._parse_summary_dict()

    @classmethod
    def from_summary(cls, summary_dict, do_full_retrieval=False):
        listing_id = summary_dict.get('listingId')
        property_id = summary_dict.get('propertyId')
        return cls(listing_id=listing_id, property_id=property_id, summary_dict=summary_dict,
                   do_full_retrieval=do_full_retrieval)

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
        self._parse_comprehensive_dict()
        return True

    def _parse_summary_dict(self):
        summary_dict = self.summary_dict

        self.house = House(
            street_address=summary_dict.get('streetLine', {}).get('value', None),
            city=summary_dict.get('city', None),
            state=summary_dict.get('state', None),
            zip=summary_dict.get('zip', None),
            square_footage=summary_dict.get('sqFt', {}).get('value', np.nan),
            lot_size=summary_dict.get('lotSize', {}).get('value', np.nan),
            bedrooms=[Bedroom() for _ in range(int(summary_dict.get('beds', 0)))],
            num_bathrooms=summary_dict.get('baths', np.nan),
            year_built=summary_dict.get('yearBuilt', {}).get('value', -1),
            list_price=summary_dict.get('price', {}).get('value', np.nan),
        )
        pass

    def _parse_comprehensive_dict(self):
        ddict = self.comprehensive_dict

        amenities_info = ddict.get('amenitiesInfo')
        if amenities_info is None:
            return

        addr_info = amenities_info.get('addressInfo')
        if addr_info is None:
            raise ValueError('Unable to find address in listing!')

        street_address = addr_info["street"]
        city = addr_info["city"]
        state = addr_info["state"]
        zip_code = int(addr_info.get("zip") or -1)
        country = addr_info["countryCode"]
        house = House(
            street_address=street_address,
            city=city,
            state=state,
            zip=zip_code,
            country=country
        )

        # Populate home info based on public records info
        if ddict.get('publicRecordsInfo') is not None:
            records_dict = ddict.get('publicRecordsInfo')
            basic_info = records_dict.get('basicInfo')
            if basic_info is not None:
                house.bedrooms = [Bedroom() for _ in range(int(basic_info.get('beds', 0)))]
                house.num_bathrooms = basic_info.get('baths', np.nan)
                house.year_built = basic_info.get('yearBuilt', -1)
                house.square_footage = basic_info.get('totalSqFt', np.nan)
                house.lot_size = basic_info.get('lotSqFt', np.nan)
                house.property_type = basic_info.get('propertyTypeName')

        # Try to populate the bedroom information more thoroughly
        bedroom_group = None
        for super_group in amenities_info.get('superGroups', []):
            for sub_group in super_group.get('amenityGroups', []):
                if 'bedroom' in sub_group.get('groupTitle', '').lower():
                    bedroom_group = sub_group
                    break
            if bedroom_group is not None:
                break
        if bedroom_group is not None:
            # Build strings to search for in the bedroom group
            test_strings = ['master'] + [f'bedroom {i+1}' for i in range(house.num_bedrooms)]

            cur_room_index = 0
            for test_string in test_strings:
                for room_dict in bedroom_group.get('amenityEntries', []):
                    room_name = room_dict.get('amenityName', '').lower()
                    if test_string in room_name and 'dimension' in room_name:
                        if cur_room_index >= house.num_bedrooms - 1:
                            house.bedrooms.append(Bedroom())
                        room = house.bedrooms[cur_room_index]
                        val = room_dict.get('amenityValues', [''])[0]
                        if len(val.split('x')) == 2:
                            room.length = int(val.split('x')[0].strip())
                            room.width = int(val.split('x')[1].strip())
                        if test_string == 'master':
                            room.is_master = True

                        # Up the room index count
                        cur_room_index += 1

            pass


        self.house = house
        pass
