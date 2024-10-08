from typing import Union

import pandas as pd

from ocean_data_qc.metadata.metadata_flag import MetadataFlag
from ocean_data_qc.metadata.metadata_qc_field import MetadataQcField


class Visit:
    METADATA_FIELDS = (
        "AIRPRES",
        "AIRTEMP",
        "COMNT_VISIT",
        "CRUISE_NO",
        "CTRYID",
        "LATIT",
        "LATIT_NOM",
        "LONGI",
        "LONGI_NOM",
        "SERNO",
        "SHIPC",
        "STATN",
        "WADEP",
        "WINDIR",
        "WINSP",
    )

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._series = self._data.SERNO.unique() if "SERNO" in self._data.columns else []
        self._station = self._data.STATN.unique() if "STATN" in self._data.columns else []
        self._times = set()
        self._positions = set()

        self._qc_fields = {
            field: MetadataFlag.NO_QC_PERFORMED for field in MetadataQcField
        }
        self._qc_log = {}

        self._init_metadata()

    def _init_metadata(self):
        self._metadata = {}

        if "SDATE" not in self._data.columns:
            self._data["SDATE"] = ""
        if "STIME" not in self._data.columns:
            self._data["STIME"] = ""

        self._times = set(
            tuple(self._data[["SDATE", "STIME"]].itertuples(index=False, name=None))
        )

        if "LATIT" in self._data.columns and "LONGI" in self._data.columns:
            self._positions = set(
                tuple(self._data[["LATIT", "LONGI"]].itertuples(index=False, name=None))
            )
        elif "LATIT_NOM" in self._data.columns and "LONGI_NOM" in self._data.columns:
            self._positions = set(
                tuple(
                    self._data[["LATIT_NOM", "LONGI_NOM"]].itertuples(
                        index=False, name=None
                    )
                )
            )

        for field in self.METADATA_FIELDS:
            if field not in self._data.columns:
                continue
            self._metadata[field] = self._data[field].unique()

    @property
    def series(self):
        return self._series

    @property
    def station(self):
        return self._station

    @property
    def qc(self):
        return self._qc_fields

    @property
    def qc_log(self):
        return self._qc_log

    def log(self, qc_field: MetadataQcField, parameters: Union[str, tuple], message: str):
        if isinstance(parameters, str):
            parameters = (parameters,)

        for parameter in parameters:
            if qc_field not in self._qc_log:
                self._qc_log[qc_field] = {parameter: []}
            if parameter not in self._qc_log[qc_field]:
                self._qc_log[qc_field][parameter] = []
            self._qc_log[qc_field][parameter].append(message)

    def water_depths(self):
        return self._data.DEPH.unique()

    def times(self):
        return self._times

    def positions(self):
        return self._positions

    @property
    def metadata(self):
        return self._metadata
