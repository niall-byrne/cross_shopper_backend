# Coding Standards for Cross Shopper

This document details the coding standards and patterns followed in the Cross Shopper codebase.

## Python Coding Style

- **Indentation:** Use 2-space indentation for all Python code.
- **Line Length:** Maximum 80 characters.
- **Docstrings:**
  - Use docstrings for modules, classes, and public methods.
  - Follow Google-style docstring conventions.
  - **Do NOT** use docstrings in test functions or fixtures; let the name be descriptive.
- **Type Hints:**
  - Use explicit type hints for all function arguments and return types.
  - Quoted string literals (e.g., `"Item"`) are preferred as type annotations to avoid circular imports.
  - Imports used ONLY for type hints MUST be placed within an `if TYPE_CHECKING:  # no cover` block.
  - Prefer types from the `typing` module (e.g., `List`, `Dict`, `Optional`) over native types for annotations.

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

## Testing Standards

- **Coverage:** Aim for 100% code coverage. Use `# no cover` for intentionally uncovered blocks (e.g., `if TYPE_CHECKING:`).
- **Pattern:** Use the strict Arrange-Act-Assert (AAA) pattern. Separate these three blocks with a single blank line.
- **Naming Convention:** Use `test_<method>__<condition1>__<condition2>__<expected_outcome>`. Use double underscores `__` to separate the method name from conditions and the outcome.
- **Fixtures:**
  - Organize `conftest.py` with general mocks at the top and testable units at the bottom.
  - Sort fixtures alphabetically within their groups.
  - Prefix mock fixtures with `mocked_`.
  - Place app-specific fixtures in `[app]/models/fixtures/` and register them in the root `conftest.py`.
- **Organization:** Use small, dedicated test files for each component (e.g., `test_item.py`).
- **Admin Testing:** Verify that all configured `ModelAdmin` attributes are correctly set.

## Project Tools

- `make fmt`: Format code using `ruff` and `yapf`.
- `make lint-python`: Run linting checks (ruff).
- `make types-python`: Run type checking (mypy).
- `make test-python`: Run the full test suite (pytest).
- `make coverage`: Run tests and verify 100% coverage.
- `make lint-markdown`: Lint markdown files.
