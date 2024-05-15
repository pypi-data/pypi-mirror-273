"""
This module contains a function `format` that modifies a BeautifulSoup object in place. It also contains two helper
functions, `parse_style` and `style_to_string`.

The `parse_style` function takes a string of CSS styles and parses it into a dictionary where keys are
CSS property names and values are the corresponding CSS values.

The `style_to_string` function takes a dictionary of CSS styles and converts it into a string representation.

The `format` function searches for all elements with the attribute "dj-style". For each found element, it parses the
existing style attributes (if any), merges them with the styles specified in "dj-style", and replaces the
style attribute with the merged styles. The values of the "dj-style" attribute are expected to be strings with pairs of
CSS properties, values, and value types separated by semicolons (;), and each triplet separated by tildes (~).
The value is inserted into the style attribute in Django template variable format (i.e., "{{ value }}").
If a value type is specified, it is appended to the value in the style attribute.
The value type can be omitted if not needed. In that case make sure to keep the semicolon at the end of the value.
Then it removes the "dj-style" attribute from the element.

Example:
    If an element is <div style="color:red" dj-style="background-color;color;px">,
    after processing, it becomes <div style="color:red;background-color:{{ color }}px">.
"""
from bs4 import BeautifulSoup


def parse_style(style: str) -> dict[str, str]:
    """
    Parses a string of CSS styles into a dictionary.

    The function takes a string where each CSS property and its corresponding value are separated by a colon,
    and each property-value pair is separated by a semicolon.
    It splits the string into key-value pairs and stores them in a dictionary.

    Args:
        style (str): A string of CSS styles.

    Returns:
        dict[str, str]: A dictionary where keys are CSS property names and values are the corresponding CSS values.

    Example:
        If the input is 'color:red;background-color:blue;',
        the output will be {'color': 'red', 'background-color': 'blue'}.
    """
    result: dict[str, str] = {}
    key_buffer = ""
    buffer = ""
    for char in style:
        if char == ":" and not key_buffer:
            key_buffer = buffer
            buffer = ""
        elif char == ";":
            result[key_buffer] = buffer
            key_buffer = ""
            buffer = ""
        elif char != " ":
            buffer += char
    if key_buffer and buffer:
        result[key_buffer] = buffer
    return result


def style_to_string(style: dict[str, str]) -> str:
    """
    Converts a dictionary of CSS styles into a string representation.

    The function takes a dictionary where keys are CSS property names and values are the corresponding CSS values.
    It joins all the items in the dictionary into a string, with each key-value pair separated by a colon and each pair
    separated by a semicolon.

    Args:
        style (dict[str, str]): A dictionary of CSS styles.

    Returns:
        str: A string representation of the CSS styles.

    Example:
        If the input is {'color': 'red', 'background-color': 'blue'},
        the output will be 'color:red;background-color:blue;'.
    """
    result = ";".join([f"{name}:{value}" for name, value in style.items()])
    if len(style) != 0:
        result += ";"
    return result


def format(soup: BeautifulSoup) -> None:
    for element in soup.find_all(attrs={"dj-style": True}):
        if element.has_attr("style"):
            style = parse_style(element["style"])
        else:
            style = {}
        dj_style = element.get("dj-style")
        for name, value, value_type in [declaration.split(";") for declaration in dj_style.split("~") if declaration]:
            style[name] = f"{{{{ {value} }}}}{value_type}"
        element["style"] = style_to_string(style)
        del element.attrs["dj-style"]
