"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for the "html" element with the attribute "dj-remove-default". If such an element is found,
the function removes the Doctype, "head" element, and "script" element within the "body" element from the BeautifulSoup
object. It also unwraps the "body" and "html" elements, leaving only the remaining content of the "body" element.

Example:
    If the html is <!DOCTYPE html><html dj-remove-default><head></head><body><script></script>Content</body></html>,
    after processing, it becomes Content.
"""
from bs4 import BeautifulSoup, Doctype, Tag


def format(soup: BeautifulSoup) -> None:
    if html := soup.find("html"):
        if isinstance(html, Tag):
            if html.has_attr("dj-remove-default"):
                if isinstance(soup.contents[0], Doctype):
                    soup.contents[0].extract()
                if head := html.find("head"):
                    if isinstance(head, Tag):
                        head.decompose()
                if body := html.find("body"):
                    if isinstance(body, Tag):
                        if script := body.find("script"):
                            if isinstance(script, Tag):
                                script.decompose()
                    body.unwrap()
                html.unwrap()
