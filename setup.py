from setuptools import setup, find_packages
import os
import re


# Read version from __version__.py
def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'systemair_api', '__version__.py'), encoding='utf-8') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Read the contents of the README file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="systemair_api",
    version=get_version(),
    description="Python library for communicating with and controlling Systemair ventilation units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Henning Berge",
    author_email="henning.ber@gmail.com",
    url="https://github.com/Promises/SystemAIR-API",
    project_urls={
        "Bug Tracker": "https://github.com/Promises/SystemAIR-API/issues",
        "Documentation": "https://github.com/Promises/SystemAIR-API#readme",
        "Source Code": "https://github.com/Promises/SystemAIR-API",
    },
    packages=find_packages(exclude=["tests", "notes"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "websocket-client",
        "beautifulsoup4",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "requests-mock",
            "black",
            "isort",
            "flake8",
            "mypy",
            "sphinx",
            "sphinx-rtd-theme",
            "sphinx-autodoc-typehints",
            "pre-commit",
            "build",
            "twine",
        ],
    },
)