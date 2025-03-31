from setuptools import setup, find_packages

setup(
    name="systemair_api",
    version="0.1.0",
    description="Python library for communicating with and controlling Systemair ventilation units",
    author="Henning Berge",
    author_email="henning.ber@gmail.com",
    url="https://github.com/Promises/SystemAIR-API",
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
)