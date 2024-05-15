from abc import ABC
from typing import Union
import pandas as pd
import numpy as np

from ._base import _BaseFormat


class _BaseColourFormat(_BaseFormat, ABC):
    def __init__(self,
                 style_kwargs):
        self.style_kwargs = style_kwargs


class ContinuousSpectrumFormat(_BaseColourFormat):
    def __init__(self,
                 min_colour,
                 max_colour,
                 mid_colour=None,
                 mid_point: Union[list, None] = None,
                 **style_kwargs) -> None:
        super().__init__(style_kwargs=style_kwargs)
        self.min_colour = min_colour
        self.max_colour = max_colour
        self.mid_colour = mid_colour
        self.mid_point = mid_point

    def create_col_config(self,
                          col_df: pd.Series):
        unique_col_values = set(col_df[~col_df.isna()])
        # Sometimes there's still np.nan values remaining - explicitly filter
        # these out
        unique_col_values = {i for i in unique_col_values if not np.isnan(i)}
        if not unique_col_values:
            return {}
        styleConditions = []
        col_min = min(unique_col_values)
        col_max = max(unique_col_values)
        for col_value in unique_col_values:
            colour = self._interpolate_color(
                value=col_value,
                min_val=col_min,
                max_val=col_max,
                min_color=self.min_colour,
                max_color=self.max_colour,
                mid_color=self.mid_colour,
                mid_point=self.mid_point
            )
            styleConditions.append(
                {
                    "condition": f"params.value == {col_value}",
                    "style": {
                        "backgroundColor": colour,
                        **self.style_kwargs
                    },
                }
            )
        return {
            'cellStyle': {
                'styleConditions': styleConditions,
            }
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)

    @staticmethod
    def _interpolate_color(value,
                           min_val,
                           max_val,
                           min_color,
                           max_color,
                           mid_color=None,
                           mid_point=None):
        """Interpolates color based on value between min and max using optional midpoint color."""
        if max_val == min_val:  # Prevent division by zero
            # Default to midpoint color or minimum color
            return mid_color if mid_color else min_color

        def hex_to_rgba(hex_color):
            """Convert hex color to an RGBA tuple."""
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 8:  # Includes alpha
                r, g, b, a = tuple(int(hex_color[i:i+2], 16)
                                   for i in (0, 2, 4, 6))
            elif len(hex_color) == 6:  # Standard RGB hex code
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                a = 255  # Default to fully opaque if alpha is not specified
            else:
                raise ValueError("Invalid hex color format")
            return (r, g, b, a)

        def rgba_to_hex(rgb):
            """Convert RGB or RGBA tuple to hex color."""
            if len(rgb) == 3:  # RGB without alpha
                return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            elif len(rgb) == 4:  # RGBA with alpha
                return '#{:02x}{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]), int(rgb[3]))
            else:
                raise ValueError("Input must be an RGB or RGBA tuple")

        def color_lerp_rgba(color1, color2, t):
            """Linearly interpolate between two RGBA colors."""
            if len(color1) != len(color2) or not (len(color1) == 3 or len(color1) == 4):
                raise ValueError(
                    "Both colors must be RGB or RGBA tuples of the same length")

            return tuple(color1[i] + (color2[i] - color1[i]) * t for i in range(len(color1)))

        # Calc mid point if not provided
        if mid_point is None:
            mid_point = (max_val + min_val) / 2
        # Convert hex to RGB
        min_color = hex_to_rgba(min_color)
        max_color = hex_to_rgba(max_color)
        # If a mid colour is provided
        if mid_color:
            mid_color = hex_to_rgba(mid_color)
            if value == mid_point:
                return rgba_to_hex(mid_color)
            elif value < mid_point:
                proportion = (value - min_val) / (mid_point - min_val)
                return rgba_to_hex(color_lerp_rgba(min_color, mid_color, proportion))
            elif value > mid_point:
                proportion = (value - mid_point) / (max_val - mid_point)
                return rgba_to_hex(color_lerp_rgba(mid_color, max_color, proportion))
        # If a mid colour isn't provided, use colour between min_color and
        # max_color
        else:
            if value <= mid_point:
                proportion = (value - min_val) / (mid_point - min_val)
                midpoint_color = color_lerp_rgba(
                    min_color, max_color, 0.5)  # Get color at mid_point
                return rgba_to_hex(color_lerp_rgba(min_color, midpoint_color, proportion))
            else:
                proportion = (value - mid_point) / (max_val - mid_point)
                midpoint_color = color_lerp_rgba(
                    min_color, max_color, 0.5)  # Get color at mid_point
                return rgba_to_hex(color_lerp_rgba(midpoint_color, max_color, proportion))


class ConditionalColourFormat(_BaseColourFormat):
    def __init__(self,
                 conditions,
                 **style_kwargs) -> None:
        super().__init__(style_kwargs=style_kwargs)
        self.conditions = conditions

    def create_col_config(self,
                          **kwargs):
        styleConditions = []
        for condition, colour in self.conditions.items():
            styleConditions.append(
                {
                    # f"params.value {condition}",
                    "condition": condition.replace('<x>', 'params.value'),
                    "style": {
                        "backgroundColor": colour,
                        **self.style_kwargs
                    },
                }
            )
        return {
            'cellStyle': {
                'styleConditions': styleConditions,
            }
        }

    def create_row_config(self,
                          *args,
                          **kwargs) -> dict:
        return super().create_row_config(*args, **kwargs)
