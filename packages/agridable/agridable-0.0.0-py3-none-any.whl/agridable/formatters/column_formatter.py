from typing import List, Literal

from ._base import _BaseColumnFormatter
from ..formats._base import _BaseFormat


class ColumnFormatter(_BaseColumnFormatter):
    def __init__(self,
                 columns: List[str],
                 formats: List[_BaseFormat],
                 if_col_not_exist: Literal['ignore', 'raise'] = 'raise') -> None:
        super().__init__(columns=columns)
        self.formats = formats
        self.if_col_not_exist = if_col_not_exist

    def format(self,
               columnDefs_dict,
               df):
        if not isinstance(self.columns, (list, set, tuple)):
            self.columns = [self.columns]
        if not isinstance(self.formats, (list, set, tuple)):
            self.formats = [self.formats]
        for col in self.columns:
            if self.if_col_not_exist == 'ignore' and col not in columnDefs_dict:
                continue
            for format in self.formats:
                format_config = format.create_col_config(
                    col_df=df[col]
                )
                for param in format_config:
                    if param in columnDefs_dict[col]:
                        columnDefs_dict[col][param] = {
                            **columnDefs_dict[col][param],
                            **format_config[param]
                        }
                    else:
                        columnDefs_dict[col][param] = format_config[param]
                # columnDefs_dict[col] = {
                #     **columnDefs_dict[col],
                #     **format.create_col_config(
                #         col_df=df[col]
                #     )
                # }
        return columnDefs_dict
