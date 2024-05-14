"""
typical IdOPVLWATER.xml content has 4 "columns":
    <map externalLocation="610" externalParameter="Q1" internalLocation="KW761001" internalParameter="Q.G.0"/>  # noqa
    <map externalLocation="612" externalParameter="HB1" internalLocation="OW761202" internalParameter="H.G.0"/>
    <map externalLocation="1001" externalParameter="FQ1" internalLocation="KW100111" internalParameter="F.0"/>
    <map externalLocation="1001" externalParameter="HS1" internalLocation="KW100110" internalParameter="H.S.0"/>
Below we defined 4 classes:
    externalLocation -> ExLocChoices
    externalParameter -> ExparChoices
    internalLocation -> IntLocChoices
    internalParameter -> IntParChoices
"""

from enum import Enum
from hdsr_wis_config_reader.idmappings.utils import get_class_attributes
from typing import List

import re


class IdMapCols:
    ex_loc = "externalLocation"  # "021"
    ex_par = "externalParameter"  # "IM1"
    int_loc = "internalLocation"  # "KW102111"
    int_par = "internalParameter"  # "DDM.d"

    @classmethod
    def get_all(cls) -> List[str]:
        return list(get_class_attributes(the_class=cls).values())


class StartEndDateCols:
    series = "series"
    start = "start"
    end = "end"
    filename_start = "filename_start"
    filename_end = "filename_end"

    @classmethod
    def get_all(cls) -> List[str]:
        return list(get_class_attributes(the_class=cls).values())


class ExLocChoices(Enum):
    """A external location is either 3 or 4 digit location. A 4 digit location can be a split location."""

    _3digit = "^[0-9]{3}$"  # 123
    _4digit = "^[0-9]{4}$"  # 1234
    _split = "^[0-9]8[0-9]{2}$"  # 1834

    @classmethod
    def is_3digit(cls, ex_loc: str) -> bool:
        assert isinstance(ex_loc, str)
        return bool(re.match(pattern=cls._3digit.value, string=ex_loc))

    @classmethod
    def is_4digit(cls, ex_loc: str) -> bool:
        assert isinstance(ex_loc, str)
        return bool(re.match(pattern=cls._4digit.value, string=ex_loc))

    @classmethod
    def _is_split_x8xx(cls, ex_loc: str) -> bool:
        assert isinstance(ex_loc, str)
        return bool(re.match(pattern=cls._split.value, string=ex_loc))

    @classmethod
    def is_split(cls, ex_loc: str) -> bool:
        assert isinstance(ex_loc, str)
        if cls._is_split_x8xx(ex_loc=ex_loc):
            return True
        # TODO: this only looks whether 2nd char is 8, but we also have to look at idmap and sub_loc
        return False


class ExParChoices(Enum):
    pass


class IntLocChoices(Enum):
    """
    in general regarding caw_complex:
        1. first digit not 0, so [1-9]
        2. second to 4 digit = [0-9]

    in general regarding hoofd, sub, ow:
        1. first digit not 0, so [1-9]
        2. second to fifth digit = [0-9]
        3. sixth digit:
          KW hoofd: 0
          KW sub: [1-9]
          OW: [0-9]

    in general regarding msw:
        1. first two digits are 76
        2. second to sixth digit [0-9]
    """

    caw_complex = "^[1-9][0-9]{3}$"
    kw_hoofd = "^KW[1-9][0-9]{4}0$"
    kw_sub = "^KW[1-9][0-9]{4}[1-9]$"
    ow = "^OW[1-9][0-9]{5}$"
    msw = "^(O|K)W76[0-9]{4}$"

    @classmethod
    def is_kw(cls, int_loc: str) -> bool:
        return True if cls.is_kw_hoofd(int_loc=int_loc) or cls.is_kw_sub(int_loc=int_loc) else False

    @classmethod
    def is_caw_complex(cls, caw_complex: str) -> bool:
        """A CAW complex is a number between 1000 and 9999"""
        assert isinstance(caw_complex, str)
        return bool(re.match(pattern=cls.caw_complex.value, string=caw_complex))

    @classmethod
    def is_kw_hoofd(cls, int_loc: str) -> bool:
        """Hoofd_locs start with 'KW' followed by 6 digits with the last being 0, eg. KW123450"""
        assert isinstance(int_loc, str)
        if cls.is_msw(int_loc=int_loc):
            return False
        return bool(re.match(pattern=cls.kw_hoofd.value, string=int_loc))

    @classmethod
    def is_kw_sub(cls, int_loc: str) -> bool:
        """Sub_locs start with 'KW' followed by 6 digits with the last not being 0, eg. KW123451"""
        assert isinstance(int_loc, str)
        if cls.is_msw(int_loc=int_loc):
            return False
        return bool(re.match(pattern=cls.kw_sub.value, string=int_loc))

    @classmethod
    def is_ow(cls, int_loc: str) -> bool:
        """OW locations start with 'OW' followed by 6 digits, eg. OW123456"""
        assert isinstance(int_loc, str)
        if cls.is_msw(int_loc=int_loc):
            return False
        return bool(re.match(pattern=cls.ow.value, string=int_loc))

    @classmethod
    def is_msw(cls, int_loc: str) -> bool:
        """MSW locations start with 'OW76' or 'KW76' followed by 4 digits, eg. KW761234 or OW761234"""
        assert isinstance(int_loc, str)
        return bool(re.match(pattern=cls.msw.value, string=int_loc))

    @classmethod
    def find_type(cls, int_loc: str) -> "IntLocChoices":
        if cls.is_msw(int_loc=int_loc):
            return cls.msw
        elif cls.is_caw_complex(caw_complex=int_loc):
            return cls.caw_complex
        elif cls.is_kw_hoofd(int_loc=int_loc):
            return cls.kw_hoofd
        elif cls.is_kw_sub(int_loc=int_loc):
            return cls.kw_sub
        elif cls.is_ow(int_loc=int_loc):
            return cls.ow


class IntParChoices(Enum):
    pass
