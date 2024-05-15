import pandas as pd
import dash_ag_grid as dag
from typing import Union, List, Tuple

from agridable.formatters._base import (
    _BaseFormatter,
    _BaseColumnFormatter,
    _BaseRowFormatter
)

DEFAULT_AG_GRID_KWARGS = {
    'className': 'ag-theme-alpine-dark',
    #  'columnSize': 'autoSize',
    'columnSize': 'responsiveSizeToFit',
    #  'columnSizeOptions': {
    #      'defaultMinWidth': 2000,
    #      'defaultMaxWidth': 200
    #  },
    'defaultColDef': {
        'filter': True,
        'floatingFilter': True,
        'suppressMenu': True,
        "resizable": True,
        "cellStyle": {
            "wordBreak": "normal",
            #     #  "lineHeight": 1,
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'textAlign': 'center'
        },
        "wrapText": True,
        "autoHeight": True,
        "wrapHeaderText": True,
        "autoHeaderHeight": True,
        "headerClass": "center-aligned-header"
    },
    'style': {
        'height': 600,
    }
}


class AGridable(dag.AgGrid):
    def __init__(self,
                 df: pd.DataFrame,
                 columns=None,
                 formatters: Union[List[_BaseFormatter], None] = None,
                 ag_grid_kwargs: dict = DEFAULT_AG_GRID_KWARGS
                 ) -> None:
        getRowStyleConditions_dict = {}
        columnDefs_dict = self._create_columnDefs_dict(df=df, columns=columns)
        columnDefs_dict = self._apply_formatters(
            df=df,
            columnDefs_dict=columnDefs_dict,
            getRowStyleConditions_dict=getRowStyleConditions_dict,
            formatters=formatters
        )
        print(columnDefs_dict)
        super().__init__(
            rowData=df.to_dict('records'),
            columnDefs=list(columnDefs_dict.values()),
            getRowStyle={
                "styleConditions": list(getRowStyleConditions_dict.values())
            },
            ** ag_grid_kwargs
        )

    @staticmethod
    def _create_columnDefs_dict(df,
                                columns):
        if columns is None:
            columns = df.columns
        return {
            col: {'field': col}
            for col in columns
        }

    @staticmethod
    def _apply_formatters(df,
                          columnDefs_dict,
                          getRowStyleConditions_dict,
                          formatters
                          ):
        if formatters is not None:
            for formatter in formatters:
                if isinstance(formatter, _BaseColumnFormatter):
                    columnDefs_dict = formatter.format(
                        columnDefs_dict=columnDefs_dict,
                        df=df
                    )
                elif isinstance(formatter, _BaseRowFormatter):
                    getRowStyleConditions_dict = formatter.format(
                        getRowStyleConditions_dict=getRowStyleConditions_dict
                    )
        return columnDefs_dict
