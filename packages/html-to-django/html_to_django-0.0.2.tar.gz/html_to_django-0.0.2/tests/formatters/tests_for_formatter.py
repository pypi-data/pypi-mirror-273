from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import for_formatter


class ForTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-for="item in list"></div>', "html.parser")
        for_formatter.format(soup)
        expected_result = "{% for item in list %}{% endfor %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-for="item in list">Test</div>', "html.parser")
        for_formatter.format(soup)
        expected_result = "{% for item in list %}Test{% endfor %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_for_inside(self) -> None:
        soup = BeautifulSoup('<div dj-for="item in list"><div dj-for="subitem in sublist">Test</div></div>',
                             "html.parser")
        for_formatter.format(soup)
        expected_result = "{% for item in list %}{% for subitem in sublist %}Test{% endfor %}{% endfor %}"
        self.assertEqual(expected_result, str(soup))
