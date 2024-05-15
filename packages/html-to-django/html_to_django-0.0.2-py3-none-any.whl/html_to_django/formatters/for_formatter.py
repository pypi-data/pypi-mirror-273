"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-for". The value of "dj-for" is expected to be a
string representing a Django template for loop. For each found element, it inserts a Django template for loop
before the element and an endfor tag after the element, using the value of "dj-for" as the loop. Then it removes
the element's original tag, leaving only the Django template for loop.

Example:
    If an element is <div dj-for="item in list"></div>,
    after processing, it becomes {% for item in list %}{% endfor %}.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-for": True}):
        element.insert_before(f"{{% for {element.get("dj-for")} %}}")
        element.insert_after("{% endfor %}")
        element.unwrap()
