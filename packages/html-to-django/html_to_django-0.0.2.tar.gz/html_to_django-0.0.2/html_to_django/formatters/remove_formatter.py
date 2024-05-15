"""
This module contains a function `format` that modifies a BeautifulSoup object in place. The function searches for
all elements with the attribute "dj-remove". For each found element, it calls the `decompose` method, which removes
the element from the parse tree. This effectively removes all elements marked with "dj-remove" from the HTML document.

Example:
    If an element is <div dj-remove></div>,
    after processing, it will be removed from the BeautifulSoup object.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-remove": True}):
        element.decompose()
