# AI Agent Instructions for Cross Shopper

Welcome, Agent. This project has strict coding and testing standards. To contribute effectively, please follow these instructions.

## Essential Reading

Before starting any task, you **MUST** read and understand:

- [CONTRIBUTING.MD](CONTRIBUTING.MD): Detailed coding and testing standards.

## Project Standards at a Glance

- **Style:** 2-space indentation, explicit type hints.
- **Testing:** Strict Arrange-Act-Assert (AAA) pattern, 100% coverage goal.
- **Naming:** `test_<method>__<condition1>__<condition2>__<expected>` naming convention, using double underscores to separate scenarios.

## Key Tools and Commands

Always use the project's tools to verify your work:

- `make fmt`: Apply formatting (ruff/yapf).
- `make lint-python`: Run linting.
- `make types-python`: Run type checking.
- `make test-python`: Run all tests.
- `make coverage`: Ensure 100% code coverage

Examine the [Makefile](Makefile) for other details.

## Contribution Workflow

1. **Understand:** Review existing tests to match the project's established patterns.
2. **Plan:** Formulate a plan that includes comprehensive testing.
3. **Implement:** Adhere to the AAA pattern and naming conventions.
4. **Verify:** Run all relevant tests and pre-commit hooks (`make fmt`, `make lint-python`).
5. **Submit:** Provide a clear summary of your changes.

## Common Pitfalls to Avoid

- **Indentation:** Ensure you use 2-space indentation. Defaulting to 4 spaces will fail linting.
- **Unused Code:** Do not leave unused fixtures in `conftest.py` or unused imports in test files.
- **Type Hints:** Use strings (e.g., `"Report"`) and minimize unnecessary imports by putting imports used only as type hints behind `if TYPE_CHECKING:  # no cover` conditionals.
- **Caching Logic:** If you modify serializers, ensure the `__repr__` method is correct and includes the required docstring for caching sharing.
- **Scope of Verification:** After refactoring, run all tests in the related directory, not just the single file you modified.

## Pro-tips for Agents

- Use `# no cover` for code blocks that cannot be tested to maintain 100% coverage reporting.
- Avoid docstrings in test functions; let the function name be descriptive.
- Extract setup and mocks to fixtures in `conftest.py` whenever possible.
- When mocking methods for caching tests, ensure the mock has a `__name__` attribute.
