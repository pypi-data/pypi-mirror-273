from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters.style_raw_formatter import format


class TestStyleRawFormat(TestCase):
    def test_format(self) -> None:
        soup = BeautifulSoup('<div dj-style-raw="color;red~width;100px" style="font-size:16px"></div>', "html.parser")
        format(soup)
        expected_result = '<div style="font-size:16px;color:red;width:100px;"></div>'
        self.assertEqual(expected_result, str(soup))

    def test_format_with_existing_style(self) -> None:
        soup = BeautifulSoup('<div dj-style-raw="color;red" style="color:blue;font-size:16px"></div>', "html.parser")
        format(soup)
        expected_result = '<div style="color:red;font-size:16px;"></div>'
        self.assertEqual(expected_result, str(soup))

    def test_format_with_no_style(self) -> None:
        soup = BeautifulSoup('<div dj-style-raw="color;red~width;100px"></div>', "html.parser")
        format(soup)
        expected_result = '<div style="color:red;width:100px;"></div>'
        self.assertEqual(expected_result, str(soup))
