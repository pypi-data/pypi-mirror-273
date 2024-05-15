from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import assets_formatter


class AssetsTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<html dj-assets="assets;module"><img src="assets/image.png"></html>', 'html.parser')
        assets_formatter.format(soup)
        expected_result = '<html><img src="{% static \'module/assets/image.png\' %}"/></html>'
        self.assertEqual(expected_result, str(soup))

    def test_empty(self) -> None:
        soup = BeautifulSoup('<html dj-assets="assets;module"></html>', 'html.parser')
        assets_formatter.format(soup)
        expected_result = '<html></html>'
        self.assertEqual(expected_result, str(soup))

    def test_no_assets(self) -> None:
        soup = BeautifulSoup('<html dj-assets="assets;module"><p>Test</p></html>', 'html.parser')
        assets_formatter.format(soup)
        expected_result = '<html><p>Test</p></html>'
        self.assertEqual(expected_result, str(soup))

    def test_with_multiple_assets(self) -> None:
        soup = BeautifulSoup('<html dj-assets="assets;module"><img src="assets/image1.png"><img '
                             'src="assets/image2.png"></html>', 'html.parser')
        assets_formatter.format(soup)
        expected_result = ('<html><img src="{% static \'module/assets/image1.png\' %}"/><img src="{% static '
                           '\'module/assets/image2.png\' %}"/></html>')
        self.assertEqual(expected_result, str(soup))
