# [MCP](https://modelcontextprotocol.io/quickstart/server) Server

Weather MCP server in python

[docs](https://modelcontextprotocol.io/quickstart/server)

[python-sdk](https://github.com/modelcontextprotocol/python-sdk)

```
# Create a new directory for our project
uv init

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create our server file
touch weather.py
```

## Testing

This project includes a comprehensive test suite for the weather service API. The tests use pytest and pytest-asyncio to test the asynchronous functions that interact with the National Weather Service API.

### Test Requirements

- Python 3.12+
- pytest
- pytest-asyncio
- pytest-cov
- httpx

### Installing Development Dependencies

You can install all development dependencies using:

```bash
# Using uv
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

### Running the Tests

To run the tests:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with code coverage
pytest --cov=weather
```

### Test Coverage

The test suite covers:

1. **Unit Tests for Helper Functions**
   - `format_alert` function for formatting alert data
   - Error handling in `make_nws_request`

2. **API Function Tests**
   - `get_alerts`: Testing successful retrieval, empty results, and API failures
   - `get_forecast`: Testing successful forecast retrieval and error handling for both API endpoints

3. **Mock Responses**
   - All HTTP requests are mocked using `httpx.AsyncMock`
   - Multiple test scenarios with different API responses

### Continuous Integration

When adding new features to the weather service, please ensure all tests pass by running the test suite before submitting changes.
