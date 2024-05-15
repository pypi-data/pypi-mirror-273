import unittest
from bs4 import BeautifulSoup
from html_to_django.formatters.if_formatter import format


class TestIfFormatter(unittest.TestCase):
    def test_format(self) -> None:
        soup = BeautifulSoup('<div dj-if="condition">Test</div>', "html.parser")
        format(soup)
        expected_result = "{% if condition %}Test{% endif %}"
        self.assertEqual(expected_result, str(soup))

    def test_format_with_elif(self) -> None:
        soup = BeautifulSoup('<div dj-if="condition1">Test</div><div dj-elif="condition2">Test2</div>', "html.parser")
        format(soup)
        expected_result = "{% if condition1 %}Test{% elif condition2 %}Test2{% endif %}"
        self.assertEqual(expected_result, str(soup))

    def test_format_with_else(self) -> None:
        soup = BeautifulSoup('<div dj-if="condition1">Test</div><div dj-else>Test2</div>', "html.parser")
        format(soup)
        expected_result = "{% if condition1 %}Test{% else %}Test2{% endif %}"
        self.assertEqual(expected_result, str(soup))

    def test_format_with_elif_and_else(self) -> None:
        soup = BeautifulSoup('<div dj-if="condition1">Test</div><div dj-elif="condition2">Test2</div>'
                             '<div dj-else>Test3</div>', "html.parser")
        format(soup)
        expected_result = "{% if condition1 %}Test{% elif condition2 %}Test2{% else %}Test3{% endif %}"
        self.assertEqual(expected_result, str(soup))
