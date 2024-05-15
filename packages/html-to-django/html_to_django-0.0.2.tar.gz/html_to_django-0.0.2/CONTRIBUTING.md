# Contributing

If you want to contribute please do it like this:
1. Create a fork of the project
2. Perform the contribution on your fork
3. Create a pull request

## Testing
- All tests must be created in the `test` directory.
- The tests should be located in a package of the same name as the code it tests.
- The name of the file should be the same as the file of the code it tests, with a `tests_` prefix.

For example, the tests for `html_to_django/formatters/attr_formatter.py` are located in `tests/formatters/tests_attr_formatter.py`.
If you make changes to the code you need to make sure all the tests are still working. Use this command to run the tests:
```bash
python -m unittest discover tests --verbose
```

## Stylechecks
Follow established python coding guidelines. To check your code you can use these commands:
```bash
mypy --strict html_to_django
pycodestyle --max-line-length 120 html_to_django
```

Change `html_to_django` to `tests` to also check your tests.
