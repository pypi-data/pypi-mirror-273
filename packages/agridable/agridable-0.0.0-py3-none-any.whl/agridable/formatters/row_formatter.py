from typing import List

from ._base import _BaseRowFormatter
from ..formats._base import _BaseFormat


class RowFormatter(_BaseRowFormatter):
    def __init__(self,
                 rows: List[int],
                 formats: List[_BaseFormat]) -> None:
        super().__init__(rows=rows)
        self.formats = formats

    def format(self,
               getRowStyleConditions_dict,
               **kwargs):
        if not isinstance(self.rows, (list, set, tuple)):
            self.rows = [self.rows]
        if not isinstance(self.formats, (list, set, tuple)):
            self.formats = [self.formats]
        for row in self.rows:
            for format in self.formats:
                if row in getRowStyleConditions_dict:
                    getRowStyleConditions_dict[row]['style'] = {
                        **getRowStyleConditions_dict[row]['style'],
                        **format.create_row_config()
                    }
                else:
                    getRowStyleConditions_dict[row] = {
                        'condition': f'params.node.rowIndex === {row}',
                        **format.create_row_config()
                    }
        return getRowStyleConditions_dict
