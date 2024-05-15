from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import var_formatter


class VarTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-var="item"></div>', "html.parser")
        var_formatter.format(soup)
        expected_result = "<div>{{ item }}</div>"
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-var="item">Test</div>', "html.parser")
        var_formatter.format(soup)
        expected_result = "<div>{{ item }}</div>"
        self.assertEqual(expected_result, str(soup))
