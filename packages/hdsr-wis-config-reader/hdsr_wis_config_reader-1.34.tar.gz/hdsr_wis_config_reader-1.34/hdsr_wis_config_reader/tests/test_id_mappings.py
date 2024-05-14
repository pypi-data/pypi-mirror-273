from hdsr_wis_config_reader import IdMappingCollection
from hdsr_wis_config_reader.constants import TEST_DIR_WIS_CONFIG
from hdsr_wis_config_reader.idmappings.columns import IdMapCols
from hdsr_wis_config_reader.idmappings.files import IdMapChoices
from hdsr_wis_config_reader.tests.fixtures import fews_config_local
from hdsr_wis_config_reader.utils import DataframeActions

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8
fews_config_local = fews_config_local


expected_df_a = pd.DataFrame(
    data={
        "externalLocation": {2880: "610", 5929: "7610"},
        "externalParameter": {2880: "Q1", 5929: "Q1"},
        "internalLocation": {2880: "KW761001", 5929: "KW761001"},
        "internalParameter": {2880: "Q.G.0", 5929: "Q.G.0"},
        "source": {2880: "IdOPVLWATER", 5929: "IdOPVLWATER"},
        "histtag": {2880: "610_Q1", 5929: "7610_Q1"},
    }
)

expected_df_b = pd.DataFrame(
    data={
        "externalLocation": {2880: "610", 5929: "7610", 2252: "610"},
        "externalParameter": {2880: "Q1", 5929: "Q1", 2252: "Q1"},
        "internalLocation": {2880: "KW761001", 5929: "KW761001", 2252: "KW761001"},
        "internalParameter": {2880: "Q.G.0", 5929: "Q.G.0", 2252: "Q.G.0"},
        "source": {2880: "IdOPVLWATER", 5929: "IdOPVLWATER", 2252: "IdOPVLWATER_HYMOS"},
        "histtag": {2880: "610_Q1", 5929: "7610_Q1", 2252: "610_Q1"},
    }
)

expected_ex_par_values = [
    "1GW",
    "GW1",
    "GW2",
    "GW3",
    "HB1",
    "HB2",
    "HB3",
    "HB4",
    "HB5",
    "HB6",
    "HB7",
    "HB8",
]


def test_idmapping_opvl_water(fews_config_local):
    id_mappings = IdMappingCollection(fews_config=fews_config_local)
    assert id_mappings.idmap_opvl_water.shape == (6050, 6)

    df_idmap_opvl_water = id_mappings.idmap_opvl_water.get_filtered_df(int_loc="KW761001")
    assert isinstance(df_idmap_opvl_water, pd.DataFrame)
    assert len(df_idmap_opvl_water) == 2
    assert DataframeActions.is_equal_dataframes(df1=expected_df_a, df2=df_idmap_opvl_water)

    ex_par_values = id_mappings.idmap_grondwater_caw.get_filtered_column_values(
        make_result_unique=True,
        target_column=IdMapCols.ex_par,
    )
    assert ex_par_values == expected_ex_par_values

    df_all = id_mappings.idmap_all.get_filtered_df(int_loc="KW761001")
    assert isinstance(df_all, pd.DataFrame)
    assert len(df_all) == 3
    assert DataframeActions.is_equal_dataframes(df1=expected_df_b, df2=df_all)


def test_read_idmap_oppvl(fews_config_local):
    # read without fews config
    oppvl_path1 = TEST_DIR_WIS_CONFIG / "IdMapFiles" / "IdOPVLWATER.xml"
    df_oppvl_without_fews = IdMappingCollection.get_idmap_df_via_path(file_path=oppvl_path1)
    assert len(df_oppvl_without_fews) == 6050

    # read same idmap but now via fews config
    collection = IdMappingCollection(fews_config=fews_config_local)
    df_oppvl_with_fews = collection.get_idmap_df_via_choice(IdMapChoices.idmap_opvl_water)
    assert DataframeActions.is_equal_dataframes(df1=df_oppvl_without_fews, df2=df_oppvl_with_fews)


def test_read_idmap_oppvl_hymos(fews_config_local):
    # read without fews config
    oppvl_path1 = TEST_DIR_WIS_CONFIG / "IdMapFiles" / "IdOPVLWATER_HYMOS.xml"
    df_oppvl_hymos_without_fews = IdMappingCollection.get_idmap_df_via_path(file_path=oppvl_path1)
    assert len(df_oppvl_hymos_without_fews) == 2360

    # read same idmap but now via fews config
    collection = IdMappingCollection(fews_config=fews_config_local)
    df_oppvl_hymos_with_fews = collection.get_idmap_df_via_choice(IdMapChoices.idmap_opvl_water_hymos)
    assert DataframeActions.is_equal_dataframes(df1=df_oppvl_hymos_without_fews, df2=df_oppvl_hymos_with_fews)
