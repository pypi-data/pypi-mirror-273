from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import block_formatter


class BlockTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-block="content"></div>', "html.parser")
        block_formatter.format(soup)
        expected_result = "{% block content %}{% endblock %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-block="content">Test</div>', "html.parser")
        block_formatter.format(soup)
        expected_result = "{% block content %}Test{% endblock %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_block_inside(self) -> None:
        soup = BeautifulSoup('<div dj-block="content"><div dj-block="inner">Test</div></div>', "html.parser")
        block_formatter.format(soup)
        expected_result = "{% block content %}{% block inner %}Test{% endblock %}{% endblock %}"
        self.assertEqual(expected_result, str(soup))
