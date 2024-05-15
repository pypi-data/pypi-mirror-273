"""
This package contains modules that define various formatters for modifying a BeautifulSoup object in place.

Each formatter module contains a `format` function that performs a specific modification on the BeautifulSoup object.

The `formatters` list in this package contains all the formatter modules for easy access and usage.
"""
from . import (for_formatter, if_formatter, var_formatter, block_formatter, static_formatter, attr_formatter,
               for_wrap_formatter, unwrap_formatter, remove_formatter, include_formatter, assets_formatter,
               remove_default_formatter, command_formatter, style_formatter, style_raw_formatter)


formatters = [for_formatter, if_formatter, var_formatter, block_formatter, static_formatter, attr_formatter,
              for_wrap_formatter, unwrap_formatter, remove_formatter, include_formatter, assets_formatter,
              remove_default_formatter, command_formatter, style_formatter, style_raw_formatter]
