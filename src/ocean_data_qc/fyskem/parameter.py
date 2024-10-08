import pandas as pd

from ocean_data_qc.fyskem.qc_flags import QcFlags


class Parameter:
    def __init__(self, data: pd.Series):
        self._data = data
        if "quality_flag_long" in data:
            self._qc = QcFlags.from_string(data["quality_flag_long"])
        else:
            self._qc = QcFlags()

    @property
    def name(self):
        return self._data.parameter

    @property
    def value(self):
        return self._data.value

    @property
    def qc(self) -> QcFlags:
        return self._qc

    @property
    def data(self):
        self._data["quality_flag_long"] = str(self._qc)
        return self._data
