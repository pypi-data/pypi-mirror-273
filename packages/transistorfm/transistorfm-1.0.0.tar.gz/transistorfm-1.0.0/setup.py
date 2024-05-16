from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "transistorfm",
    version = "1.0.0",
    author = "Josh Griffiths",
    author_email = "josh@hakuna.co.uk",
    description = "A Python client for the Transistor.fm API",
    license = "MIT",
    requires=['requests'],
    long_description_content_type="text/markdown",
    long_description=long_description
)