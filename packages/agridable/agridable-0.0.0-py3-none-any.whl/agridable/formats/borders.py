from ._base import _BaseFormat


class Border(_BaseFormat):
    def __init__(self,
                 border_side='bottom',
                 border_width='1px',
                 border_style='solid',
                 border_colour='white'
                 ):
        self.border_side = border_side
        self.border_width = border_width
        self.border_style = border_style
        self.border_colour = border_colour
        self.border_side = f'border{self.border_side.title()}'
        self.border_prop = f'{self.border_width} {self.border_style} {self.border_colour}'

    def create_col_config(self,
                          *args,
                          **kwargs) -> dict:
        return {
            'cellStyle': {
                self.border_side: self.border_prop
            },
        }

    def create_row_config(self,
                          *args,
                          **kwargs):
        return {
            'style': {
                self.border_side: self.border_prop
            }
        }
