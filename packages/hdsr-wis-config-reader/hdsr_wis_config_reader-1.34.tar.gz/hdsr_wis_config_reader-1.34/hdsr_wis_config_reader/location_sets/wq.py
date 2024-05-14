from hdsr_wis_config_reader.location_sets.base import LocationSetBase
from typing import List


class WaterQualityLocationSet(LocationSetBase):
    @property
    def name(self):
        return "waterquality"

    @property
    def fews_name_candidates(self) -> List[str]:
        return ["OPVLWATER_WQLOC", "OW_WQ"]

    @property
    def idmap_section_name(self):
        return ""

    @property
    def skip_check_location_set_error(self):
        return True

    @property
    def validation_rules(self):
        return []
