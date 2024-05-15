"""
This module contains a function `format` that modifies a BeautifulSoup object in place.

The `format` function searches for all elements with the attribute "dj-unwrap". For each found element, it removes the
element's tags but keeps its content.

Example:
    If an element is <div dj-unwrap><p>Hello, world!</p></div>,
    after processing, it becomes <p>Hello, world!</p>.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-unwrap": True}):
        element.unwrap()
