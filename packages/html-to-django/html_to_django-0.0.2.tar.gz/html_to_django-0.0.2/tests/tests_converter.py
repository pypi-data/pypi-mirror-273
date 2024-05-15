import os
import filecmp
import shutil
import tempfile
import sys
from io import StringIO
from unittest import TestCase
from bs4 import BeautifulSoup
from glob import glob
from typing import Any
from html_to_django.converter import get_required_libraries, convert_file, convert_dir, convert_path


class TestDirectory(tempfile.TemporaryDirectory):  # type: ignore
    """
    Context Manager that creates a temporary directory containing the test project.
    """
    def __enter__(self) -> Any:
        tmpdir = super().__enter__()
        shutil.copytree(
            "tests/test_project",
            tmpdir,
            dirs_exist_ok=True
        )
        return tmpdir


class ConverterTests(TestCase):
    def test_get_required_libraries(self) -> None:
        html = '<div dj-libs="lib1;lib2">Content</div><div dj-libs="lib3"></div>'
        soup = BeautifulSoup(html, 'html.parser')
        expected = {'lib1', 'lib2', 'lib3'}
        self.assertEqual(expected, get_required_libraries(soup))

    def test_get_required_libraries_empty(self) -> None:
        html = '<div>Content</div>'
        soup = BeautifulSoup(html, 'html.parser')
        expected: set[str] = set()
        self.assertEqual(expected, get_required_libraries(soup))

    def test_convert_file(self) -> None:
        with TestDirectory() as tmpdir:
            convert_file(f"{tmpdir}/test.html")
            # verify that the new file exists and has the expected value
            self.assertTrue(filecmp.cmp(
                "tests/test_project_expected_result/test.html",
                f"{tmpdir}/test.n.html"
            ))
            # verify that the source file is unchanged
            self.assertTrue(filecmp.cmp(
                "tests/test_project/test.html",
                f"{tmpdir}/test.html"
            ))

    def test_convert_file_overwrite(self) -> None:
        with TestDirectory() as tmpdir:
            convert_file(f"{tmpdir}/test.html", True)
            # verify that the source file has been overwriten
            self.assertTrue(filecmp.cmp(
                "tests/test_project_expected_result/test.html",
                f"{tmpdir}/test.html"
            ))
            # verify that no new file was created
            self.assertFalse(os.path.exists(f"{tmpdir}/test.n.html"))

    def test_convert_file_non_html_extension(self) -> None:
        with TestDirectory() as tmpdir:
            os.rename(f"{tmpdir}/test.html", f"{tmpdir}/test.txt")

            convert_file(f"{tmpdir}/test.txt")
            # verify that the source file has been overwriten
            self.assertTrue(filecmp.cmp(
                "tests/test_project_expected_result/test.html",
                f"{tmpdir}/test.n.txt"
            ))

    def test_convert_file_no_extension(self) -> None:
        with TestDirectory() as tmpdir:
            os.rename(f"{tmpdir}/test.html", f"{tmpdir}/test")

            convert_file(f"{tmpdir}/test")
            # verify that the source file has been overwriten
            self.assertTrue(filecmp.cmp(
                "tests/test_project_expected_result/test.html",
                f"{tmpdir}/test.n"
            ))

    def test_convert_file_nonexistent(self) -> None:
        with self.assertRaises(FileNotFoundError):
            convert_file("tests/test/project/nonexistent_file.html")

    def test_convert_file_dir_passed(self) -> None:
        with self.assertRaises(FileNotFoundError):
            convert_file("tests/test_project")

    def test_convert_dir(self) -> None:
        with TestDirectory() as tmpdir:
            convert_dir(f"{tmpdir}")

            for conversion_result in glob(f"{tmpdir}/**/*.n.html", recursive=True):
                conversion_source = conversion_result.replace(".n.html", ".html")

                # verify that the new file exists and has the expected value
                expected_result = conversion_source.replace(tmpdir, "tests/test_project_expected_result")
                self.assertTrue(filecmp.cmp(
                    expected_result,
                    conversion_result
                ))

                # verify that the source file is unchanged
                original_source = conversion_source.replace(tmpdir, "tests/test_project")
                self.assertTrue(filecmp.cmp(
                    original_source,
                    conversion_source
                ))

    def test_convert_dir_overwrite(self) -> None:
        with TestDirectory() as tmpdir:
            convert_dir(f"{tmpdir}", True)

            for conversion_result in glob(f"{tmpdir}/**/*.html", recursive=True):
                # verify that the source file has been overwritten
                expected_result = conversion_result.replace(tmpdir, "tests/test_project_expected_result")
                self.assertTrue(filecmp.cmp(
                    expected_result,
                    conversion_result
                ))

                # verify that no new file was created
                self.assertFalse(os.path.exists(conversion_result.replace(".html", ".n.html")))

    def test_convert_dir_nonexistent(self) -> None:
        with self.assertRaises(FileNotFoundError):
            convert_dir("tests/test_project/nonexistent_folder")

    def test_convert_dir_file_passed(self) -> None:
        with self.assertRaises(FileNotFoundError):
            convert_dir("tests/test_project/test.html")

    def test_convert_path_file(self) -> None:
        with TestDirectory() as tmpdir:
            convert_path(f"{tmpdir}/test.html")
            # verify that the new file exists and has the expected value
            self.assertTrue(filecmp.cmp(
                "tests/test_project_expected_result/test.html",
                f"{tmpdir}/test.n.html"
            ))
            # verify that the source file is unchanged
            self.assertTrue(filecmp.cmp(
                "tests/test_project/test.html",
                f"{tmpdir}/test.html"
            ))

    def test_convert_path_file_overwrite(self) -> None:
        with TestDirectory() as tmpdir:
            convert_path(f"{tmpdir}/test.html", True)
            # verify that the source file has been overwriten
            self.assertTrue(filecmp.cmp(
                "tests/test_project_expected_result/test.html",
                f"{tmpdir}/test.html"
            ))
            # verify that no new file was created
            self.assertFalse(os.path.exists(f"{tmpdir}/test.n.html"))

    def test_convert_path_dir(self) -> None:
        with TestDirectory() as tmpdir:
            convert_path(f"{tmpdir}")

            for conversion_result in glob(f"{tmpdir}/**/*.n.html", recursive=True):
                conversion_source = conversion_result.replace(".n.html", ".html")

                # verify that the new file exists and has the expected value
                expected_result = conversion_source.replace(tmpdir, "tests/test_project_expected_result")
                self.assertTrue(filecmp.cmp(
                    expected_result,
                    conversion_result
                ))

                # verify that the source file is unchanged
                original_source = conversion_source.replace(tmpdir, "tests/test_project")
                self.assertTrue(filecmp.cmp(
                    original_source,
                    conversion_source
                ))

    def test_convert_path_dir_overwrite(self) -> None:
        with TestDirectory() as tmpdir:
            convert_path(f"{tmpdir}", True)

            for conversion_result in glob(f"{tmpdir}/**/*.html", recursive=True):
                # verify that the source file has been overwritten
                expected_result = conversion_result.replace(tmpdir, "tests/test_project_expected_result")
                self.assertTrue(filecmp.cmp(
                    expected_result,
                    conversion_result
                ))

                # verify that no new file was created
                self.assertFalse(os.path.exists(conversion_result.replace(".html", ".n.html")))

    def test_convert_path_nonexistent(self) -> None:
        with self.assertRaises(SystemExit) as cm:
            convert_path("tests/test/project/nonexistent_file.html")

        expected_result = 'The path "tests/test/project/nonexistent_file.html" does not exist.'
        self.assertIn(expected_result, cm.exception.args)
