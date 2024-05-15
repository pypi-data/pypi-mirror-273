from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import command_formatter


class CommandTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-command="command_name"></div>', "html.parser")
        command_formatter.format(soup)
        expected_result = "{% command_name %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-command="command_name">Test</div>', "html.parser")
        command_formatter.format(soup)
        expected_result = "{% command_name %}"
        self.assertEqual(expected_result, str(soup))
