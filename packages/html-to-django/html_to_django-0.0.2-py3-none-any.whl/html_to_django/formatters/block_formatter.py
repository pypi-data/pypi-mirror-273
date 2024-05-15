"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-block". The value of "dj-block" is expected to be a
string representing the name of a Django block. For each found element, it inserts Django block tags before and after
the element, using the value of "dj-block" as the block name. Then it removes the "dj-block" attribute from the element.

Example:
    If an element is <div dj-block="content">Content</div>,
    after processing, it becomes {% block content %}Content{% endblock %}.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-block": True}):
        element.insert_before(f"{{% block {element.get("dj-block")} %}}")
        element.insert_after("{% endblock %}")
        element.unwrap()
