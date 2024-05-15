"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-for-wrap". The value of "dj-for-wrap" is expected to be a
string representing a Django template for loop. For each found element, it inserts a Django template for loop
before the element and an endfor tag after the element, using the value of "dj-for-wrap" as the loop. Then it removes
the "dj-for-wrap" attribute from the element, leaving the element wrapped in the Django template for loop.

Example:
    If an element is <div dj-for-wrap="item in list">Content</div>,
    after processing, it becomes {% for item in list %}<div>Content</div>{% endfor %}.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-for-wrap": True}):
        element.insert_before(f"{{% for {element.get("dj-for-wrap")} %}}")
        element.insert_after("{% endfor %}")
        del element["dj-for-wrap"]
