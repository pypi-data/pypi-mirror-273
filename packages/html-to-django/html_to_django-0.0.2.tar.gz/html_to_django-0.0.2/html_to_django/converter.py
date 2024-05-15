import bs4
import sys
import os
from typing import Literal
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Namespace
from glob import glob
from .formatters import formatters


def get_required_libraries(soup: bs4.BeautifulSoup) -> set[str]:
    """
    Extracts the required libraries from a BeautifulSoup object.

    The function searches for all elements with the attribute "dj-libs". For each found element, it adds the values of
    the "dj-libs" attribute to a set. The values are expected to be library names separated by semicolons (;).
    Then it removes the "dj-libs" attribute from the element.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the HTML to extract the libraries from.

    Returns:
        set[str]: A set of strings representing the names of the required libraries.

    Example:
        If the input is <div dj-libs="lib1;lib2">Content</div><div dj-libs="lib3"></div>,
        the function returns {'lib1', 'lib2', 'lib3'}.
    """
    libs = set()
    for element in soup.find_all(attrs={"dj-libs": True}):
        libs |= set(element.get("dj-libs").split(";"))
        del element.attrs["dj-libs"]
    return libs


def convert_file(path: str, overwrite: bool = False) -> None:
    """
    Converts the special attributes in an HTML file to Django template tags.

    The function reads the HTML file, parses it into a BeautifulSoup object, and applies a series of formatters to it.
    The formatters modify the BeautifulSoup object in place, adding Django template tags based on special attributes
    in the HTML. The function also extracts the required libraries from the BeautifulSoup object and writes them at the
    top of the output file.
    The output file is either the original file (if overwrite is True) or a new file with the same name but an
    additional ".n" before the ".html" extension (if overwrite is False).

    Args:
        path (str): The path to the HTML file to be converted.
        overwrite (bool, optional): Whether to overwrite the original file. Defaults to False.
    """
    if not (os.path.exists(path) and os.path.isfile(path)):
        raise FileNotFoundError

    with open(path, "r") as file:
        soup = bs4.BeautifulSoup(file, "html.parser")

    required_libraries = get_required_libraries(soup)

    for formatter in formatters:
        formatter.format(soup)

    if overwrite:
        out_path = path
    else:
        filename, file_extension = os.path.splitext(path)
        out_path = f"{filename}.n{file_extension}"
    with open(out_path, "w") as file:
        for lib in required_libraries:
            file.write(f"{{% load {lib} %}}\n")
        file.write(soup.prettify(formatter=bs4.formatter.HTMLFormatter(indent=4)))


def convert_dir(path: str, overwrite: bool = False) -> None:
    """
    Converts the special attributes in all HTML files in a directory to Django template tags.

    The function traverses the directory recursively and applies the `convert_file` function to each HTML file it finds.

    Args:
        path (str): The path to the directory containing the HTML files to be converted.
        overwrite (bool, optional): Whether to overwrite the original files. Defaults to False.
    """
    if not (os.path.exists(path) and os.path.isdir(path)):
        raise FileNotFoundError

    for filepath in glob(f"{path}/**/*.html", recursive=True):
        convert_file(filepath, overwrite)


def parse_args(name: Literal["html_to_django", "html_to_django_r"]) -> Namespace:
    description = "Converts special attributes in HTML files to Django template tags."
    if name == "html_to_django_r":
        description = ("Info: This command is identical to html_to_django, but will always replace the input file(s)!"
                       f"\n\n{description}")

    parser = ArgumentParser(name, description=description, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("path", help="""
    The path to a file (or folder of files) to be converted.
    In case a folder is passed, ALL html files in it (recursively) will be converted.
    """, type=str)

    if name == "html_to_django":
        parser.add_argument("-r", "--replace", help="""
        Replace the input file(s).
        """, action='store_true')

    return parser.parse_args()


def convert_path(path: str, overwrite: bool = False) -> None:
    """
    Converts the special attributes in the HTML files at the given path to Django template tags.

    The function determines whether the provided path is a directory or a file.
    If it's a file, it applies the `convert_file` function to convert the file.
    If it's a directory, it applies the `convert_dir` function to convert all HTML files in the directory.
    If the provided path does not exist, the function exits the program with an error message.

    Args:
        path (str): The path to a file or a directory of files to be converted. If a directory is passed, all HTML files
                    in it (recursively) will be converted.
        overwrite (bool): A flag indicating whether to replace the input files. If this flag is set, the original HTML
                          files are overwritten with the converted Django templates. If this flag is not set, the
                          converted Django templates are written to new files, and the original HTML files are left
                          unchanged.
    """
    if os.path.isdir(path):
        convert_dir(path, overwrite)
    elif os.path.isfile(path):
        convert_file(path, overwrite)
    else:
        sys.exit(f'The path "{path}" does not exist.')


def command_entry() -> None:
    """
    Entry point for the command line interface of the html_to_django tool.

    The function parses the command line arguments and calls `convert_path` with the parsed arguments.

    The command line arguments are:

    path: The path to a file or a directory of files to be converted. If a directory is passed, all HTML files in it
    (recursively) will be converted.

    replace (optional): A flag indicating whether to replace the input files. If this flag is set, the original HTML
    files are overwritten with the converted Django templates. If this flag is not set, the converted Django templates
    are written to new files, and the original HTML files are left unchanged.
    """
    args = parse_args("html_to_django")
    convert_path(args.path, args.replace)


def command_entry_r() -> None:
    """
    Entry point for the command line interface of the html_to_django_r tool.

    This function is identical to `command_entry`, but it always overwrites the original HTML files.

    The command line argument is:

    path: The path to a file or a directory of files to be converted. If a directory is passed, all HTML files in it
    (recursively) will be converted.
    """
    args = parse_args("html_to_django_r")
    convert_path(args.path, True)
