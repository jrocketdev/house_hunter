from dataclasses import dataclass, field
from typing import List
import numpy as np

@dataclass
class Bedroom:
    width: float = np.nan
    length: float = np.nan
    is_master: bool = False
    has_attached_bathroom: bool = False
    has_vaulted_ceilings: bool = False

    @property
    def square_footage(self):
        return self.width*self.length

@dataclass
class Bathroom:
    width: float = np.nan
    length: float = np.nan

@dataclass
class House:
    street_address: str
    city: str
    state: str
    zip: int

    square_footage: float = np.nan
    lot_size: float = np.nan
    bedrooms: List[Bedroom] = field(default_factory=list)
    num_bathrooms: float = np.nan
    stories: int = -1
    description: str = ''

    has_ac: bool = False
    has_heat: bool = False
    has_solar: bool = False

    property_type: str = None
    year_built: int = None

    list_price: float = np.nan
    mls_num: int = -1
    country: str = 'US'

    @property
    def num_bedrooms(self):
        return len(self.bedrooms)
