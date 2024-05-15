from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import unwrap_formatter


class UnwrapTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-unwrap><div>Test</div></div>', "html.parser")
        unwrap_formatter.format(soup)
        expected_result = "<div>Test</div>"
        self.assertEqual(expected_result, str(soup))

    def test_empty(self) -> None:
        soup = BeautifulSoup('<div dj-unwrap></div>', "html.parser")
        unwrap_formatter.format(soup)
        expected_result = ""
        self.assertEqual(expected_result, str(soup))

    def test_with_unwrap_inside(self) -> None:
        soup = BeautifulSoup('<div dj-unwrap><div dj-unwrap>Inner Test</div></div>', "html.parser")
        unwrap_formatter.format(soup)
        expected_result = "Inner Test"
        self.assertEqual(expected_result, str(soup))
