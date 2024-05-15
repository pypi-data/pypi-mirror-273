"""
This module contains a function `format` that modifies a BeautifulSoup object in place.

The `format` function searches for all elements with the attribute "dj-style-raw". For each found element, it parses the
existing style attributes (if any), merges them with the styles specified in "dj-style-raw", and replaces the
style attribute with the merged styles. The values of the "dj-style-raw" attribute are expected to be strings with pairs
of CSS properties and values separated by semicolons (;), and each pair separated by tildes (~).
Unlike the `style_formatter` module, this module does not insert the values into the style attribute in Django template
variable format. Then it removes the "dj-style-raw" attribute from the element.

Example:
    If an element is <div style="color:red" dj-style-raw="background-color;blue">,
    after processing, it becomes <div style="color:red;background-color:blue">.
"""
from bs4 import BeautifulSoup
from .style_formatter import parse_style, style_to_string


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-style-raw": True}):
        if element.has_attr("style"):
            style = parse_style(element["style"])
        else:
            style = {}
        dj_style = element.get("dj-style-raw")
        for name, value in [declaration.split(";") for declaration in dj_style.split("~") if declaration]:
            style[name] = value
        element["style"] = style_to_string(style)
        del element.attrs["dj-style-raw"]
