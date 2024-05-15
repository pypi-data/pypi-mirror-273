import unittest
from bs4 import BeautifulSoup
from html_to_django.formatters.attr_formatter import format


class TestAttrFormatter(unittest.TestCase):
    def test_format(self) -> None:
        soup = BeautifulSoup('<div dj-attr="class;my_class"></div>', "html.parser")
        format(soup)
        expected_result = '<div class="{{ my_class }}"></div>'
        self.assertEqual(expected_result, str(soup))

    def test_format_multiple(self) -> None:
        soup = BeautifulSoup('<div dj-attr="class;my_class~id;my_id"></div>', "html.parser")
        format(soup)
        expected_result = '<div class="{{ my_class }}" id="{{ my_id }}"></div>'
        self.assertEqual(expected_result, str(soup))

    def test_format_overwrite_existing(self) -> None:
        soup = BeautifulSoup('<div class="original_class" dj-attr="class;new_class"></div>', "html.parser")
        format(soup)
        expected_result = '<div class="{{ new_class }}"></div>'
        self.assertEqual(expected_result, str(soup))
