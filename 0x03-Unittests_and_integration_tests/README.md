# 0x03. Unittests and Integration Tests

This directory contains unit tests and integration tests for Python functions and classes using the unittest framework.

## Files

- `utils.py` - Utility functions including access_nested_map, get_json, and memoize decorator
- `client.py` - GithubOrgClient class for interacting with GitHub API
- `fixtures.py` - Test fixtures for integration tests
- `test_utils.py` - Unit tests for utility functions
- `test_client.py` - Unit tests and integration tests for GithubOrgClient
- `requirements.txt` - Required Python packages
- `run_tests.py` - Test runner script

## Requirements

- Python 3.7+
- parameterized
- requests

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

To run all tests:
```bash
python run_tests.py
```

To run specific test files:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

## Test Cases

### test_utils.py
1. **TestAccessNestedMap.test_access_nested_map** - Tests access_nested_map function with various nested dictionaries
2. **TestAccessNestedMap.test_access_nested_map_exception** - Tests that KeyError is raised for invalid paths
3. **TestGetJson.test_get_json** - Tests get_json function with mocked HTTP requests
4. **TestMemoize.test_memoize** - Tests memoize decorator functionality

### test_client.py
1. **TestGithubOrgClient.test_org** - Tests GithubOrgClient.org method
2. **TestGithubOrgClient.test_public_repos_url** - Tests _public_repos_url property
3. **TestGithubOrgClient.test_public_repos** - Tests public_repos method
4. **TestGithubOrgClient.test_has_license** - Tests has_license static method
5. **TestIntegrationGithubOrgClient** - Integration tests with fixtures

## Features

- Parameterized tests using @parameterized.expand
- Mocking HTTP requests with unittest.mock
- Property mocking for testing memoized properties
- Integration tests with fixtures
- Comprehensive test coverage for all methods