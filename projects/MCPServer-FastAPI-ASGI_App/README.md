# MCP Server in a FastAPI ASGI Application

## Fast API

FastAPI is a modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints.

## Uvicorn

[Uvicorn](https://www.uvicorn.org/) is an [ASGI](https://asgi.readthedocs.io/en/latest/) web server implementation for Python.

---

```shell
uv pip install fastapi uvicorn
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

```shell
uvicorn main:app --reload
```
