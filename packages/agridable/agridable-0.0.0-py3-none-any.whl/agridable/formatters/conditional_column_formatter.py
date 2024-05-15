from typing import List, Literal

from ._base import _BaseColumnFormatter


class ConditionalColumnFormatter(_BaseColumnFormatter):
    def __init__(self,
                 columns,
                 conditions,
                 if_col_not_exist: Literal['ignore', 'raise'] = 'raise') -> None:
        super().__init__(columns=columns)
        self.conditions = conditions
        self.if_col_not_exist = if_col_not_exist
        # {('colA', 2): Format}

    def format(self,
               columnDefs_dict,
               **kwargs):
        for col in self.columns:
            if self.if_col_not_exist == 'ignore' and col not in columnDefs_dict:
                continue
            func_args = []
            for (condition_col, condition_value), format in self.conditions.items():
                format_function = format._create_format_function()
                func_args.append(
                    f'params.data["{condition_col}"], {condition_value}, {format_function}'
                )
            func = f'conditionalFormat({",".join(func_args)})'
            columnDefs_dict[col] = {
                **columnDefs_dict[col],
                "valueFormatter": {
                    "function": func
                },
            }
        return columnDefs_dict
