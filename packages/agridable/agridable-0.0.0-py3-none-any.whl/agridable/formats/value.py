from abc import ABC, abstractmethod
from typing import Union, Literal

from ._base import _BaseFormat

CURRENCY_CODES = [
    'USD',
    'EUR',
    'GBP',
]
PRECISION_TYPE_JS_MAP = {
    'dp': 'f',
    'sf': 'r'
}


class _BaseValueFormat(_BaseFormat, ABC):
    def __init__(self) -> None:
        super().__init__()

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        format_function = self._create_format_function()
        return {
            "valueFormatter": {
                "function": format_function
            },
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)

    @abstractmethod
    def _create_format_function(self):
        pass


class Percentage(_BaseValueFormat):
    def __init__(self,
                 precision: int = 2,
                 precision_type: Literal['sf', 'dp'] = 'dp',
                 is_decimal: Literal['true', 'false'] = 'true'):
        self.precision = precision
        self.precision_type = precision_type
        self.is_decimal = is_decimal
        self.precision_type_js = PRECISION_TYPE_JS_MAP[self.precision_type]

    def _create_format_function(self):
        return f'formatPercentage(params.value, {self.precision}, "{self.precision_type_js}", {self.is_decimal})'


class Currency(_BaseValueFormat):
    def __init__(self,
                 currency: str = 'USD',
                 precision: int = 2,
                 precision_type: Literal['sf', 'dp'] = 'dp',
                 unit_scale: Union[
                     Literal['thousands', 'millions',
                             'billions', 'trillion'], None
                 ] = None):
        self.currency = currency
        self.precision = precision
        self.precision_type = precision_type
        self.precision_type_js = PRECISION_TYPE_JS_MAP[self.precision_type]
        self.unit_scale = unit_scale

    def _create_format_function(self):
        return f'formatCurrency(params.value, "{self.currency}", "{self.unit_scale}", {self.precision}, "{self.precision_type_js}")'


class Number(_BaseValueFormat):
    def __init__(self,
                 precision: int = 2,
                 precision_type: Literal['sf', 'dp'] = 'dp',
                 unit_scale: Union[
                     Literal['thousands', 'millions',
                             'billions', 'trillion'], None
                 ] = None):
        self.precision = precision
        self.precision_type = precision_type
        self.precision_type_js = PRECISION_TYPE_JS_MAP[self.precision_type]
        self.unit_scale = unit_scale

    def _create_format_function(self):
        return f'formatNumber(params.value, "{self.unit_scale}", {self.precision}, "{self.precision_type_js}")'


class NumberWithPrefixSuffix(_BaseValueFormat):
    def __init__(self,
                 prefix="null",
                 suffix="null",
                 precision: int = 2,
                 precision_type: Literal['sf', 'dp'] = 'dp',
                 unit_scale: Union[
                     Literal['thousands', 'millions',
                             'billions', 'trillion'], None
                 ] = None):
        self.prefix = prefix
        self.suffix = suffix
        self.precision = precision
        self.precision_type = precision_type
        self.precision_type_js = PRECISION_TYPE_JS_MAP[self.precision_type]
        self.unit_scale = unit_scale

    def _create_format_function(self):
        return f'formatNumberPrefixSuffix(params.value, {self.prefix}, {self.suffix}, "{self.unit_scale}", {self.precision}, "{self.precision_type_js}")'


class Duration(_BaseValueFormat):
    def __init__(self,
                 unit='minutes',
                 output_unit='minutes') -> None:
        self.unit = unit
        self.output_unit = output_unit

    def _create_format_function(self):
        return f'formatDuration(params.value, "{self.unit}", "{self.output_unit}")'


class Url(_BaseFormat):
    def __init__(self):
        pass

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            "cellRenderer": 'formatUrl'
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)


class Image(_BaseFormat):
    def __init__(self):
        pass

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            "cellRenderer": 'formatImg'
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)
