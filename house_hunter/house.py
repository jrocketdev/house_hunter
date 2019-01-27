from dataclasses import dataclass, field
from typing import List
import numpy as np

@dataclass
class Room:
    width: float = np.nan
    length: float = np.nan
    is_master: bool = False
    has_attached_bathroom: bool = False
    has_vaulted_ceilings: bool = False

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
    square_footage: int
    lot_size: float = np.nan
    rooms: List[Room] = field(default_factory=list)
    bathrooms: List[Bathroom] = field(default_factory=list)
    stories: int = -1
    description: str = ''

    has_ac: bool = False
    has_heat: bool = False
    has_solar: bool = False

    property_type: str = None
    year_built: int = None

    list_price: float = np.nan
    mls_num: int = -1
