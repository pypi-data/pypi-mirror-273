from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import static_formatter


class StaticTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<img dj-static="src;image.png"/>', "html.parser")
        static_formatter.format(soup)
        expected_result = '<img src="{% static \'image.png\' %}"/>'
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-static="background;image.png">Test</div>', "html.parser")
        static_formatter.format(soup)
        expected_result = '<div background="{% static \'image.png\' %}">Test</div>'
        self.assertEqual(expected_result, str(soup))
