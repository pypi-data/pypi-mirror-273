from enum import Enum
from hdsr_wis_config_reader.idmappings.sections import SectionTypeChoices
from hdsr_wis_config_reader.location_sets.base import LocationSetBase
from typing import List


class HoofdLocTypeChoices(Enum):
    waterstand = "waterstand"
    peilschaal = "peilschaal"
    hoofdlocatie = "hoofdlocatie"

    @classmethod
    def get_all(cls):
        return [x.value for x in cls.__members__.values()]


class HoofdLocationSet(LocationSetBase):
    @property
    def name(self):
        return "hoofdlocaties"

    @property
    def fews_name_candidates(self) -> List[str]:
        return ["OPVLWATER_HOOFDLOC", "OW_HL"]

    @property
    def idmap_section_name(self):
        return SectionTypeChoices.kunstwerken.value

    @property
    def skip_check_location_set_error(self):
        return False

    @property
    def validation_rules(self):
        return [
            {
                "parameter": "H.S.",
                "extreme_values": {"hmax": "HS1_HMAX", "hmin": "HS1_HMIN"},
            },
            {
                "parameter": "H2.S.",
                "extreme_values": {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"},
            },
            {
                "parameter": "H3.S.",
                "extreme_values": {"hmax": "HS3_HMAX", "hmin": "HS3_HMIN"},
            },
        ]
