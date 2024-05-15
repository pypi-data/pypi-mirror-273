"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-static". The value of "dj-static" is expected to be a
string representing a tag and a static file path separated by a semicolon. For each found element, it replaces the value
of the specified tag with a Django template static command, using the specified static file path.
Then it removes the "dj-static" attribute from the element.

Example:
    If an element is <img dj-static="src;images/pic.jpg">,
    after processing, it becomes <img src="{% static 'images/pic.jpg' %}">.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-static": True}):
        tag, value = element.get("dj-static").split(";")
        element[tag] = f"{{% static '{value}' %}}"
        del element.attrs["dj-static"]
