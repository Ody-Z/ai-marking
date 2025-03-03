# Tests for Homework Marking System

This directory contains unit tests for the Homework Marking System.

## Running Tests

To run all tests:

```bash
cd backend
python -m unittest discover tests
```

To run a specific test file:

```bash
cd backend
python -m unittest tests.services.test_pdf_processor
```

## Structure

- `tests/services/`: Tests for service classes
- `tests/resources/`: Test resource files

## Adding New Tests

Follow these guidelines when adding new tests:

1. Create test files with a naming pattern of `test_*.py`
2. Each test class should inherit from `unittest.TestCase`
3. Use descriptive test method names that start with `test_`
4. Use mocks for external dependencies
5. Include assertions to verify expected behavior 