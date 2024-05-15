import unittest
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from html_to_django.formatters.remove_default_formatter import format


class TestFormatFunction(unittest.TestCase):
    # The strings here look weird because of the indentation and line breaks, but it must be this way
    def test_basic(self) -> None:
        html = """<!DOCTYPE html>
        <html lang="en" dj-remove-default>
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
                <h1>
                    Test
                </h1>
                <script src="test.js">
                </script>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        format(soup)
        expected_result = "<h1>\n    Test\n</h1>\n"
        self.assertEqual(expected_result, soup.prettify(formatter=HTMLFormatter(indent=4)))
