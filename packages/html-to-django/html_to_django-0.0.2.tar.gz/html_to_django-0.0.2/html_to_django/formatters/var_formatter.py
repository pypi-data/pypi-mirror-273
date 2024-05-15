"""
This module contains a function `format` that modifies a BeautifulSoup object in place.

The `format` function searches for all elements with the attribute "dj-var". For each found element, it replaces the
element's content with a Django template variable that has the same name as the value of the "dj-var" attribute.
Then it removes the "dj-var" attribute from the element.

Example:
    If an element is <p dj-var="greeting">Hello, world!</p>,
    after processing, it becomes <p>{{ greeting }}</p>.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-var": True}):
        element.string = f"{{{{ {element.get("dj-var")} }}}}"
        del element.attrs["dj-var"]
