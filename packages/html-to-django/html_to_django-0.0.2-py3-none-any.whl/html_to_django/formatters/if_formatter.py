"""
This module contains a function `format` that modifies a BeautifulSoup object in place.
The function searches for all elements with the attribute "dj-if". The value of "dj-if" is expected to be a
string representing a Django template if condition. For each found element, it inserts a Django template if tag
before the element. If there are subsequent siblings with "dj-elif" or "dj-else" attributes, it also processes them
appropriately to form a complete Django template if-elif-else structure. Then it removes the original tags, leaving
only the Django template if-elif-else structure.

Example:
    If the elements are <div dj-if="condition1">Test</div><div dj-elif="condition2">Test2</div><div dj-else>Test3</div>,
    after processing, they become {% if condition1 %}Test{% elif condition2 %}Test2{% else %}Test3{% endif %}.
"""
from bs4 import BeautifulSoup


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-if": True}):
        element.insert_before(f"{{% if {element.get("dj-if")} %}}")

        participating_blocks = [element]

        current_sibling = element.find_next_sibling()
        while current_sibling is not None:
            if current_sibling.has_attr("dj-elif"):
                current_sibling.insert_before(f"{{% elif {current_sibling.get("dj-elif")} %}}")
                participating_blocks.append(current_sibling)
                current_sibling = current_sibling.find_next_sibling()
            elif current_sibling.has_attr("dj-else"):
                current_sibling.insert_before("{% else %}")
                participating_blocks.append(current_sibling)
                current_sibling = None
            else:
                current_sibling = None

        participating_blocks[-1].insert_after("{% endif %}")

        for block in participating_blocks:
            block.unwrap()
