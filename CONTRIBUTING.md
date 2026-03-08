# Contributing to Cross Shopper

Thank you for your interest in contributing to Cross Shopper! To maintain high code quality and consistency, please follow these guidelines.

## Code Style

- **Indentation:** Use 2-space indentation for all Python code.
- **Docstrings:** Use docstrings for modules, classes, and public methods. Avoid them in test functions and fixtures.
- **Caching Pattern:** When implementing caching, use the custom `memoize` decorator. Methods intended for cross-instance caching MUST have a custom `__repr__` and include the docstring: `"""Control caching behaviour across instances."""`.
- **Sentinels:** Use unique sentinel classes (e.g., `CacheMiss`) instead of `None` to distinguish between a missing value and a present `None`.

## Running the Test Suite

To run the tests you will need to create a `.env` file and initialize values for:

- `DJANGO_SECRET_KEY`

To execute all tests `make test` is the most straight-forward mechanism.

## Testing Standards

We strive for 100% code coverage. If a block of code is intentionally not covered (e.g., `if TYPE_CHECKING:`), use `# pragma: no cover`.

### Test Naming Convention

Follow the `test_<method>__<condition1>__<condition2>__<expected_outcome>` convention. Separate each scenario or condition with a double underscore. Use descriptive names instead of docstrings in test functions.

### Arrange, Act, Assert (AAA)

Organize your tests into three distinct blocks separated by a single blank line:

1. **Arrange:** Set up the test conditions.
2. **Act:** Perform the action under test.
3. **Assert:** Group all assertions at the end of the test.

### Formatting

- **Arguments:** Format function arguments one per line in test definitions.

### Type Hints

- Use explicit type hints for all function arguments and return types.
- Quoted string literals are preferred as type annotations.
- If an import is ONLY used as a type hint, it MUST go behind an `if TYPE_CHECKING:  # no cover` conditional.
- Types imported from `typing` are preferred to native types. i.e. `Dict`, `List`, `Sequence`, `Mapping`, etc., should be imported from `typing`.

### Fixtures and `conftest.py`

- Organize `conftest.py` with general mocks at the top and testable units at the bottom.
- Within these groups, sort fixtures alphabetically.
- Prefix mocks with `mocked_`.
- Check and remove any unused imports or fixtures to keep test files clean.

## Making Changes

1. **Pre-commit Hooks:** Always run pre-commit hooks before submitting your changes.
   - `make fmt`: Format your code using `ruff` and `yapf`.
   - `make lint-python`: Run linting checks.
   - `make types-python`: Run type checking.
2. **Testing:** Ensure all tests pass.
   - `make test-python`: Run all tests.
   - `make coverage`: Check code coverage.
3. **Commits:** Use descriptive commit messages.
