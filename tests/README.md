# Tests Directory

This directory contains unit tests and integration tests for the Carbon AI Microservice project.

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_preprocessing.py

# Run with coverage
pytest --cov=src tests/
```

## Test Structure

- `test_preprocessing.py` - Tests for data preprocessing functions
- `conftest.py` - PyTest configuration and fixtures

## Adding New Tests

When adding new functionality, please add corresponding tests to maintain code quality and reliability.
