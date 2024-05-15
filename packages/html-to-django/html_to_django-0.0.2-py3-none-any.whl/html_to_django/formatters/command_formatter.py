"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-command". The value of "dj-command" is expected to be a
string representing a Django template command. For each found element, it replaces the element's content with the Django
template command, using the value of "dj-command" as the command. Then it removes the element's original tag, leaving
only the Django template command.

Example:
    If an element is <div dj-command="url 'index'"></div>,
    after processing, it becomes {% url 'index' %}.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-command": True}):
        element.string = f"{{% {element.get("dj-command")} %}}"
        element.unwrap()
