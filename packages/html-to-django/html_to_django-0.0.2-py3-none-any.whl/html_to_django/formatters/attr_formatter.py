"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-attr".
The value of "dj-attr" is expected to be a string with pairs of attributes and values separated by semicolons (;),
and each pair separated by tildes (~). For each found element, it splits the "dj-attr" value into attribute-value pairs,
formats the value into a Django template variable format (i.e., "{{ value }}"), and assigns it to the corresponding
attribute of the element. After processing all attribute-value pairs, it removes the "dj-attr" attribute from
the element.

Example:
    If an element is <div dj-attr="class;my-class~id;my-id"></div>,
    after processing, it becomes <div class="{{ my-class }}" id="{{ my-id }}"></div>.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-attr": True}):
        for attribute, value in [pair.split(";") for pair in element["dj-attr"].split("~")]:
            element[attribute] = f"{{{{ {value} }}}}"
        del element.attrs["dj-attr"]
