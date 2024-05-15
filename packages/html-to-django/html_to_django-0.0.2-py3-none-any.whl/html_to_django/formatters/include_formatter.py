"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-include". The value of "dj-include" is expected to be a
string representing a Django template include command. For each found element, it replaces the element's content with
the Django template include command, using the value of "dj-include" as the command.
Then it removes the "dj-include" attribute from the element.

Example:
    If an element is <div dj-include="template_name.html"></div>,
    after processing, it becomes {% include "template_name.html" %}.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-include": True}):
        element.string = f'{{% include "{element.get("dj-include")}" %}}'
        del element.attrs["dj-include"]
