import pandas
from IPython.display import display

display_options = {
    'wide': 'display.max_columns',
    'long': 'display.max_rows',
    'uncut': 'display.max_colwidth',
}

def patch():
    def _validate(opts):
        invalid = list(set(opts) - set(display_options))
        if invalid:
            raise ValueError(
                f'{invalid} not in valid display options: {list(display_options)}'
            )

    def _display(self, *opts):
        _validate(opts)
        options = sum([[display_options[opt], None] for opt in opts], [])
        with pandas.option_context(*options):
            display(self)
    
    pandas.core.generic.NDFrame.display = _display
    pandas.core.generic.NDFrame.long = lambda frame: _display(frame, 'long')
    pandas.core.generic.NDFrame.wide = lambda frame: _display(frame, 'wide')
    pandas.core.generic.NDFrame.uncut = lambda frame: _display(frame, 'uncut')
    pandas.core.generic.NDFrame.full = lambda frame: _display(frame, *display_options)

__all__ = ['patch']
