from abc import ABC
from typing import Literal

from ._base import _BaseFormat


class _BaseStructureFormat(_BaseFormat, ABC):
    def __init__(self) -> None:
        super().__init__()


class Pin(_BaseStructureFormat):
    def __init__(self,
                 side: Literal['left', 'right'] = 'left'):
        self.side = side

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            'pinned': self.side
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)


class Width(_BaseStructureFormat):
    def __init__(self,
                 width=None,
                 min_width=None,
                 max_width=None,
                 suppress_size_to_fit=True) -> None:
        super().__init__()
        self.width = width
        self.min_width = min_width
        self.max_width = max_width
        self.suppress_size_to_fit = suppress_size_to_fit

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            'width': self.width,
            'minWidth': self.min_width,
            'maxWidth': self.max_width,
            'suppressSizeToFit': self.suppress_size_to_fit
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)


class Align(_BaseStructureFormat):
    def __init__(self,
                 h_align: Literal['left', 'center', 'right'] = 'center',
                 v_align: Literal['start', 'center', 'end'] = 'center') -> None:
        super().__init__()
        self.h_align = h_align
        self.v_align = v_align

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            'cellStyle': {
                'textAlign': self.h_align,
                'justifyContent': self.h_align,
                'display': 'flex',
                'alignItems': self.v_align,
            }
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)


class HeaderAlign(_BaseStructureFormat):
    def __init__(self,
                 alignment: Literal['left', 'center', 'right']) -> None:
        super().__init__()
        self.alignment = alignment

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            'headerClass': f'{self.alignment}-aligned-header'
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)
