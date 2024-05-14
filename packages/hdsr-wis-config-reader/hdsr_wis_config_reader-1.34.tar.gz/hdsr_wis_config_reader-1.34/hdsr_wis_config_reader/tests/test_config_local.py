from hdsr_wis_config_reader.tests.fixtures import fews_config_local
from hdsr_wis_config_reader.tests.test_config_production import _validate_loc_sets

import logging
import pandas as pd  # noqa pandas comes with geopandas
import pytest


# silence flake8
fews_config_local = fews_config_local

logger = logging.getLogger(__name__)


expected_df_parameter_column_names = [
    "DESCRIPTION",
    "GROUP",
    "ID",
    "NAME",
    "PARAMETERTYPE",
    "SHORTNAME",
    "UNIT",
    "USESDATUM",
    "VALUERESOLUTION",
]


@pytest.mark.second_to_last  # run this test second_to_last as it takes long (~3 min)!
def test_local_fews_config(fews_config_local):
    fews_config = fews_config_local
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets

    _validate_loc_sets(fews_config, loc_sets)

    # test FewsConfigReader parameters (special case that works different for old configs and new configs)
    df_parameters = fews_config_local.get_parameters()
    assert isinstance(df_parameters, pd.DataFrame)
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names
