# Contributing to Cross Shopper

Thank you for your interest in contributing to Cross Shopper! To maintain high code quality and consistency, please follow these guidelines.

## Code Style

- **Indentation:** Use 2-space indentation for all Python code.
- **Line Length:** Maximum 80 characters.
- **Docstrings:**
  - Use docstrings for modules, classes, and public methods.
  - Follow Google-style docstring conventions.
  - **Do NOT** use docstrings in test functions or fixtures; let the name be descriptive.
- **Type Hints:**
  - Use explicit type hints for all function arguments and return types.
  - If an import is ONLY used as a type hint, it MUST go behind an `if TYPE_CHECKING:` conditional.

## Django & Django Rest Framework (DRF) Patterns

### Models

- Validation logic should be implemented in the `clean()` method.
- Use `ModelBase` as the base class for models where applicable.

### Serializers

- **Upsert Operations:** Implement upserts by overriding the `create` method and using `update_or_create`. Disable default unique-together validators by overriding `get_unique_together_validators` to return an empty list.
- **Naming:** Generally use plural names for fields representing collections (e.g., `items`, `stores`).
- **N+1 Prevention:** Use `prefetch_related` in ViewSets.

### Admin

- **Attributes:** Define attributes like `list_filter`, `search_fields`, `readonly_fields`, and `ordering` directly within the `ModelAdmin` subclass.
- **Organization:** Modularize admin logic into subdirectories like `inlines/`, `list_displays/`, and `list_filters/`.
- **Ordering:** Prefer the static `ordering` attribute over the `get_ordering` method when the sort order is constant.

### Filtering

- Use `DefaultFilterSet` to define default values for missing query parameters using `default_<field_name>` methods.
- Use `PassThroughFilter` to pass query parameters directly to serializers.

## Caching

- **Decorator:** Use the custom `@memoize` decorator for caching method results.
- **Cross-Instance Caching:**
  - Methods intended for cross-instance caching MUST have a custom `__repr__` that includes all identifying state.
  - These `__repr__` methods MUST include the docstring: `"""Control caching behaviour across instances."""`.
- **Sentinels:** Use unique sentinel classes (e.g., `CacheMiss`) instead of `None` to distinguish between a missing value and a cached `None`.
- **Leaks:** Avoid `functools.cache` on instance methods to prevent memory leaks; use `@memoize` instead.

## Running the Test Suite

To run the tests you will need to create a `.env` file and initialize values for:

- `DJANGO_SECRET_KEY`

To run all tests `make test` is the most straight-forward mechanism.

### Test Naming Convention

Follow the `test_<method>__<condition1>__<condition2>__<expected_outcome>` convention. Separate each scenario or condition with a double underscore. Use descriptive names instead of docstrings in test functions.

### Arrange, Act, Assert (AAA)

Organize your tests into three distinct blocks separated by a single blank line:

1. **Arrange:** Set up the test conditions.
2. **Act:** Perform the action under test.
3. **Assert:** Group all assertions at the end of the test.

### Formatting

- **Arguments:** Format function arguments one per line in test definitions.

### Fixtures and `conftest.py`

- Organize `conftest.py` with general mocks at the top and testable units at the bottom.
- Within these groups, sort fixtures alphabetically.
- Prefix mocks with `mocked_`.
- Place app-specific fixtures in `[app]/models/fixtures/` and register them in the root `conftest.py`.
- Check and remove any unused imports or fixtures to keep test files clean.

### Organization

- Use small, dedicated test files for each component (e.g., `test_item.py`).
- **Admin Testing:** Verify that all configured `ModelAdmin` attributes are correctly set.

## Making Changes

1. **Pre-commit Hooks:** Always run pre-commit hooks before submitting your changes.
   - `make fmt`: Format your code using `ruff` and `yapf`.
   - `make lint-python`: Run linting checks.
   - `make types-python`: Run type checking.
   - `make lint-markdown`: Lint markdown files.
2. **Testing:** Ensure all tests pass.
   - `make test-python`: Run all tests.
   - `make coverage`: Check code coverage.
3. **Commits:** Use descriptive commit messages.
