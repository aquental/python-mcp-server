from setuptools import setup

setup(
    name="python-mcp-server",
    version="0.1.0",
    description="A simple MCP server to query DeFi data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["weather", "main"],  # Explicitly list the top-level modules
    python_requires=">=3.12.6",
    install_requires=[
        "httpx>=0.28.1",
        "mcp[cli]>=1.6.0",
    ],
    # Additional metadata
    author="",
    author_email="",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
