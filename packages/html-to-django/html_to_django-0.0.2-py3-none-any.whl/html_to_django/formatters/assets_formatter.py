"""
This module contains a function `format` that modifies a BeautifulSoup object in place. The function searches for
the "html" element with the attribute "dj-assets". The value of "dj-assets" is expected to be a string with two parts
separated by a semicolon (;), the first part being the asset identifier and the second part being the asset prefix.

For each element in the BeautifulSoup object with a "href" or "src" attribute that starts with the asset identifier,
it adds the asset prefix to the attribute value and wraps it in a Django static command.


After processing all elements, it removes the "dj-assets" attribute from the "html" element.

Example:
    If the "html" element is <html dj-assets="assets;module">...</html>,
    and there is an element <img src="assets/image.png">,
    after processing, the "img" element becomes <img src="{% static 'module/assets/image.png' %}">.
"""
from bs4 import BeautifulSoup, Tag


def format(soup: BeautifulSoup) -> None:
    if html := soup.find("html"):
        if isinstance(html, Tag):
            if html.has_attr("dj-assets"):
                if isinstance(html["dj-assets"], str):
                    asset_identifier, asset_prefix = html["dj-assets"].split(";")
                    for element in soup.find_all(attrs={"href": True}):
                        if element["href"].startswith(asset_identifier):
                            element["href"] = f"{{% static '{asset_prefix}/{element['href']}' %}}"
                    for element in soup.find_all(attrs={"src": True}):
                        if element["src"].startswith(asset_identifier):
                            element["src"] = f"{{% static '{asset_prefix}/{element['src']}' %}}"
                    del html["dj-assets"]
