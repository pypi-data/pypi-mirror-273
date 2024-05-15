from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import remove_formatter


class RemoveTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-remove><div>Test</div></div>', "html.parser")
        remove_formatter.format(soup)
        expected_result = ""
        self.assertEqual(expected_result, str(soup))

    def test_empty(self) -> None:
        soup = BeautifulSoup('<div dj-remove></div>', "html.parser")
        remove_formatter.format(soup)
        expected_result = ""
        self.assertEqual(expected_result, str(soup))

    def test_with_remove_inside(self) -> None:
        soup = BeautifulSoup('<div dj-remove><div dj-remove>Inner Test</div></div>', "html.parser")
        remove_formatter.format(soup)
        expected_result = ""
        self.assertEqual(expected_result, str(soup))
