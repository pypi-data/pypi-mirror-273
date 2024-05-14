from hdsr_wis_config_reader.readers.xml_reader import XmlReader
from hdsr_wis_config_reader.utils import PdReadFlexibleCsv
from pathlib import Path
from shapely.geometry import Point
from typing import Dict
from typing import Optional

import geopandas as gpd
import logging
import os
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


class FewsConfigReader:
    xyz_columns = {"x": "X", "y": "Y", "z": ""}
    geo_datum = {"Rijks Driehoekstelsel": "epsg:28992"}
    Z_NODATA_VALUE = -9999

    def __init__(self, path: Path):
        self.path = path
        self._location_sets = None

        # FEWS config dir-structure
        self.CoefficientSetsFiles = dict()
        self.DisplayConfigFiles = dict()
        self.FlagConversionsFiles = dict()
        self.IconFiles = dict()
        self.IdMapFiles = dict()
        self.MapLayerFiles = dict()
        self.ModuleConfigFiles = dict()
        self.ModuleDatasetFiles = dict()
        self.PiClientConfigFiles = dict()
        self.RegionConfigFiles = dict()
        self.ReportTemplateFiles = dict()
        self.RootConfigFiles = dict()
        self.SystemConfigFiles = dict()
        self.UnitConversionsFiles = dict()
        self.WorkflowFiles = dict()

        # checks and populate config dir-structure
        self._validate_constructor()
        self._populate_files()
        self._validate_minimal_config_exists()

    def _validate_constructor(self):
        assert isinstance(self.path, Path), f"path {self.path} must be a pathlib.Path"
        assert self.path.is_dir(), f"path {self.path} must be an existing directory"

    def _populate_files(self) -> None:
        """Set all fews config filepaths (.xml, .shx, etc) on self.

        Example result:
            self.CoefficientSetsFiles = {
                'BovenkantBuis': WindowsPath('.../FEWS_SA/config/CoefficientSetsFiles/BovenkantBuis.xml'),
                'DebietParameters': WindowsPath('.../FEWS_SA/config/CoefficientSetsFiles/DebietParameters.xml')
                },
            self.DisplayConfigFiles = {
                'GridDisplay': WindowsPath('../FEWS_SA/config/DisplayConfigFiles/GridDisplay.xml'),
                'ManualForecastDisplay': WindowsPath('.../FEWS_SA/config/DisplayConfigFiles/ManualForecastDisplay.xml'),
                'SystemMonitorDisplay': WindowsPath('.../FEWS_SA/config/DisplayConfigFiles/SystemMonitorDisplay.xml'),
                etc..
                },
            etc..
        """
        for dirpath, dirnames, filenames in os.walk(self.path):
            _dirpath = Path(dirpath)
            if _dirpath == self.path:
                continue
            if _dirpath.name not in self.__dict__.keys():
                continue
            for filename in filenames:
                filename_no_suffix = Path(filename).stem
                full_path = _dirpath / filename
                logger.debug(f"populate FewsConfig with property {_dirpath.name} for file {filename_no_suffix}")
                self.__dict__[_dirpath.name].update({filename_no_suffix: full_path})
        logger.info("finished populating FEWS config files")

    def _validate_minimal_config_exists(self):
        assert self.MapLayerFiles
        assert self.IdMapFiles
        assert self.RegionConfigFiles
        required_region_config_files = ["LocationSets", "Parameters"]
        for required_file in required_region_config_files:
            if not self.RegionConfigFiles.get(required_file, None):
                raise AssertionError(f"{required_file} must be in WIS config {self.path}")

    @property
    def location_sets(self) -> Dict:
        if self._location_sets is not None:
            return self._location_sets
        location_dict = XmlReader.xml_to_dict(xml_filepath=self.RegionConfigFiles["LocationSets"])
        location_sets = location_dict["locationSets"]["locationSet"]
        self._location_sets = {
            location_set["id"]: {key: value for key, value in location_set.items() if key != "id"}
            for location_set in location_sets
        }
        return self._location_sets

    def __get_parameter_the_old_way(self) -> pd.DataFrame:
        parameters_dict = XmlReader.xml_to_dict(xml_filepath=self.RegionConfigFiles["Parameters"])
        parameters = parameters_dict["parameters"]
        result_dict = {}
        for group in parameters["parameterGroups"]["parameterGroup"]:
            if isinstance(group["parameter"], dict):
                group["parameter"] = [group["parameter"]]
            for parameter in group["parameter"]:
                result_dict.update({parameter["id"]: {}})
                result_dict[parameter["id"]] = {key: value for key, value in parameter.items() if key != "id"}
                result_dict[parameter["id"]].update({key: value for key, value in group.items() if key != "parameter"})
                result_dict[parameter["id"]]["groupId"] = result_dict[parameter["id"]].pop("id")

        # put the stuff from Daniel Tollenaar in dataframe to align with __get_parameter_the_new_way (very ugly code..)
        rename_mapper = {
            # column in parameters.csv : tag in parameters.xml
            "GROUP": "groupId",
            "DESCRIPTION": "Diepte tov bovenkant buis",  # let op deze is optioneel in parameters.xml
            "PARAMETERTYPE": "parameterType",
            "UNIT": "unit",
            "VALUERESOLUTION": "valueResolution",
            "USESDATUM": "usesDatum",
            "ID": "",  # "--> dit is de parameter zelf!
            "NAME": "name",
            "SHORTNAME": "shortName",
        }

        df_parameters = pd.DataFrame(columns=rename_mapper.keys())
        row_id = 0
        for parameter, _dict in result_dict.items():
            # 'B.d': {
            #   'shortName': 'Biomassa productie [kg/ha] - dag',
            #   'name': 'Biomassa productie [kg/ha] - dag',
            #  'parameterType': 'instantaneous',
            #  'unit': 'kg/ha',
            #  'valueResolution': '0.1',
            #  'groupId': 'Biomassa'
            #  },
            new_row = []
            for df_col_name, dict_name in rename_mapper.items():
                value = _dict.get(dict_name, "")
                new_row.append(value)
            df_parameters.loc[row_id] = new_row
            df_parameters.loc[row_id, "ID"] = parameter
            row_id += 1
        return df_parameters

    def __get_parameter_the_new_way(self) -> pd.DataFrame:
        parameters_csv_path = self.MapLayerFiles["parameters"]
        reader = PdReadFlexibleCsv(path=parameters_csv_path)
        return reader.df

    def get_parameters(self) -> pd.DataFrame:
        """Extract a dictionary of parameter(groups) from a FEWS-config. Some waterboards define parameters in a
        csv file that is read into a parameters.xml. However, HDSR directly defines it in a parameters.xml
        Update August 2021
                1) before August 2021 parameters were in RegionConfigFiles/Parameters.xml
                2) afterward they were relocated to MapLayerFiles/parameters.csv
        Returns e.g. ['B.d', 'B.m', 'B.y', 'MsApr1.a', 'Rh.C.0', 'Rh.5', 'Rh.10', 'Rh.15', 'Rh.h', 'Rh.d', ...]
        """
        try:
            return self.__get_parameter_the_old_way()
        except Exception as err:
            logger.warning(
                f"could not get parameters from old location (RegionConfigFiles/Parameters.xml) "
                f"Trying new location (MapLayerFiles/parameters.csv), err={err}"
            )
        return self.__get_parameter_the_new_way()

    @classmethod
    def __add_geometry_column(
        cls,
        gdf: gpd.GeoDataFrame,
        filepath: Path,
        x_column: str,
        y_column: str,
        z_column: str = None,
    ) -> gpd.GeoDataFrame:
        """Add geometry column to geodataframe by merging geodataframe columns x, y, and z:
        -   if column z_attrib exists and has empty cells ('') with z=Z_NODATA_VALUE.
            NOTE: we leave the original empty cells (z_column) empty
        -   if column z_attrib does not exists? then we use z=Z_NODATA_VALUE -9999 for all rows."""
        assert (x_column and y_column) in gdf.columns, f"x={x_column} and y={y_column} must be in df"
        original_columns = gdf.columns
        tmp_z_column = "tmp_z_column"
        assert isinstance(cls.Z_NODATA_VALUE, int), f"Z_NODATA_VALUE {cls.Z_NODATA_VALUE} must be integer"

        gdf[tmp_z_column] = cls.Z_NODATA_VALUE

        if z_column:
            # tmp fix to handle legacy (-9999 instead of pd.NA)
            mask_9999 = gdf[z_column].isin(
                [
                    cls.Z_NODATA_VALUE,
                    str(cls.Z_NODATA_VALUE),
                    str(float(cls.Z_NODATA_VALUE)),
                ]
            )
            if sum(mask_9999):
                raise AssertionError(f"found nodata values (replace '-9999' with '') in {filepath}")

            assert gdf[z_column].dtype == "O"
            mask_tmp_z_fill = gdf[z_column].isin(["", gpd.pd.NA])
            nr_tmp_z_fill = sum(mask_tmp_z_fill)
            if nr_tmp_z_fill:
                logger.debug(
                    f"using default value Z_NODATA_VALUE {cls.Z_NODATA_VALUE} for {nr_tmp_z_fill} "
                    f"(out of {len(gdf)}) rows"
                )
                gdf[tmp_z_column] = gdf[z_column]
                # gdf[tmp_z_column][mask_tmp_z_fill] = str(cls.Z_NODATA_VALUE)
                gdf.loc[mask_tmp_z_fill, tmp_z_column] = str(cls.Z_NODATA_VALUE)

        try:
            gdf["geometry"] = gdf.apply(
                func=(
                    lambda x: Point(
                        float(x[x_column]),
                        float(x[y_column]),
                        float(x[tmp_z_column]),
                    )
                ),
                axis=1,
            )
            return gdf[original_columns]
        except Exception as err:
            logger.warning(f"could not create xyz, err={err}")
            for index, row in gdf.iterrows():
                try:
                    Point(
                        float(row[x_column]),
                        float(row[y_column]),
                        float(row[tmp_z_column]),
                    )
                except Exception as err:
                    msg = (
                        f"could not create xyz in gdf row {index}: x={row[x_column]}, y={row[y_column]}, "
                        f"z={row[z_column]}, err={err}, file={filepath}"
                    )
                    raise AssertionError(msg)

    def get_locations(self, location_set_key: str) -> Optional[gpd.GeoDataFrame]:
        """Convert FEWS locationSet locations into df. Args 'location_set_key' (str) is e.g. 'OPVLWATER_HOOFDLOC'."""
        assert isinstance(location_set_key, str)
        location_set = self.location_sets.get(location_set_key, None)
        if not location_set:
            logger.warning(f"no location_set found in fews_config for location_set_key: {location_set_key}")
            return

        file = location_set.get("csvFile", {}).get("file", None)
        if not file:
            logger.warning(f"found location_set but not file in fews_config for location_set_key: {location_set_key}")
            return

        file = Path(file)
        if not file.suffix:
            file = file.parent / (file.name + ".csv")
        filepath = self.path / "MapLayerFiles" / file

        assert filepath.is_file(), f"file {filepath} does not exist"
        gdf_loc_set = self.get_gdf_locset_via_path(file_path=filepath, xyz_columns={}, location_set=location_set)
        return gdf_loc_set

    @classmethod
    def get_gdf_locset_via_path(
        cls, file_path: Path, location_set: Dict = None, xyz_columns: Dict = None
    ) -> gpd.GeoDataFrame:
        xyz_columns = xyz_columns if xyz_columns else cls.xyz_columns
        gdf_location_set = gpd.read_file(filename=file_path)
        x_column = location_set["csvFile"]["x"].replace("%", "") if location_set else xyz_columns["x"]
        assert x_column and isinstance(x_column, str)
        y_column = location_set["csvFile"]["y"].replace("%", "") if location_set else xyz_columns["y"]
        assert y_column and isinstance(y_column, str)
        # z column does not always exist
        z_column = location_set["csvFile"].get("z", "").replace("%", "") if location_set else xyz_columns.get("z", "")
        assert isinstance(z_column, str)

        gdf_location_set = cls.__add_geometry_column(
            gdf=gdf_location_set,
            filepath=file_path,
            x_column=x_column,
            y_column=y_column,
            z_column=z_column,
        )
        geo_datum_found = location_set["csvFile"]["geoDatum"] if location_set else ""
        crs = cls.geo_datum.get(geo_datum_found, None)
        gdf_location_set.crs = crs if crs else None
        return gdf_location_set
