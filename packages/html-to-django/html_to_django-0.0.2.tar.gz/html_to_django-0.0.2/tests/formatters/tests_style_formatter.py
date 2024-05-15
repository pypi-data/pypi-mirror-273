from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters.style_formatter import parse_style, style_to_string, format


class TestParseStyle(TestCase):
    def test_parse_style(self) -> None:
        style = "color:red;background-color:blue;width:100px"
        expected_result = {
            "color": "red",
            "background-color": "blue",
            "width": "100px"
        }
        self.assertEqual(expected_result, parse_style(style))

    def test_parse_style_ending_semicolon(self) -> None:
        style = "color:red;background-color:blue;width:100px;"
        expected_result = {
            "color": "red",
            "background-color": "blue",
            "width": "100px"
        }
        self.assertEqual(expected_result, parse_style(style))

    def test_parse_style_with_spaces(self) -> None:
        style = "color: red ; background-color: blue ; width: 100px"
        expected_result = {
            "color": "red",
            "background-color": "blue",
            "width": "100px"
        }
        self.assertEqual(expected_result, parse_style(style))

    def test_parse_style_empty(self) -> None:
        style = ""
        expected_result: dict[str, str] = {}
        self.assertEqual(expected_result, parse_style(style))


class TestStyleToString(TestCase):
    def test_style_to_string(self) -> None:
        style = {
            "color": "red",
            "background-color": "blue",
            "width": "100px"
        }
        expected_result = "color:red;background-color:blue;width:100px;"
        self.assertEqual(expected_result, style_to_string(style))

    def test_style_to_string_with_empty_dict(self) -> None:
        style: dict[str, str] = {}
        expected_result = ""
        self.assertEqual(expected_result, style_to_string(style))


class TestFormat(TestCase):
    def test_format(self) -> None:
        soup = BeautifulSoup('<div dj-style="color;color;~background-color;background_color;~width;100;px"'
                             'style="font-size:16px"></div>', "html.parser")
        format(soup)
        expected_result = ('<div style="font-size:16px;color:{{ color }};background-color:{{ background_color }};'
                           'width:{{ 100 }}px;"></div>')
        self.assertEqual(expected_result, str(soup))

    def test_format_overwriting_existing_style(self) -> None:
        soup = BeautifulSoup('<div dj-style="color;color;~width;100;px" style="color:blue;font-size:16px"></div>',
                             "html.parser")
        format(soup)
        expected_result = '<div style="color:{{ color }};font-size:16px;width:{{ 100 }}px;"></div>'
        self.assertEqual(expected_result, str(soup))

    def test_format_with_no_style(self) -> None:
        soup = BeautifulSoup('<div dj-style="color;color;~width;100;px"></div>', "html.parser")
        format(soup)
        expected_result = '<div style="color:{{ color }};width:{{ 100 }}px;"></div>'
        self.assertEqual(expected_result, str(soup))
