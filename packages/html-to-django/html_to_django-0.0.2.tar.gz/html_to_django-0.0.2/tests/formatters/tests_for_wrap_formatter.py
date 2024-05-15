from unittest import TestCase
from bs4 import BeautifulSoup
from html_to_django.formatters import for_wrap_formatter


class ForWrapTests(TestCase):
    def test_basic(self) -> None:
        soup = BeautifulSoup('<div dj-for-wrap="item in list"></div>', "html.parser")
        for_wrap_formatter.format(soup)
        expected_result = "{% for item in list %}<div></div>{% endfor %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_content(self) -> None:
        soup = BeautifulSoup('<div dj-for-wrap="item in list">Test</div>', "html.parser")
        for_wrap_formatter.format(soup)
        expected_result = "{% for item in list %}<div>Test</div>{% endfor %}"
        self.assertEqual(expected_result, str(soup))

    def test_with_for_wrap_inside(self) -> None:
        soup = BeautifulSoup('<div dj-for-wrap="item in list"><div dj-for-wrap="subitem in sublist">Test</div></div>',
                             "html.parser")
        for_wrap_formatter.format(soup)
        expected_result = ("{% for item in list %}<div>{% for subitem in sublist %}<div>Test</div>{% endfor %}"
                           "</div>{% endfor %}")
        self.assertEqual(expected_result, str(soup))
