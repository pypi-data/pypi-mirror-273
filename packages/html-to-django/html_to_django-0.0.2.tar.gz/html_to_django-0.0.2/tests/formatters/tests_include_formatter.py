from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import include_formatter


class IncludeTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-include="template_name"></div>', "html.parser")
        include_formatter.format(soup)
        expected_result = '<div>{% include "template_name" %}</div>'
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-include="template_name">Test</div>', "html.parser")
        include_formatter.format(soup)
        expected_result = '<div>{% include "template_name" %}</div>'
        self.assertEqual(expected_result, str(soup))
