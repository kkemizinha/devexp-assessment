from setuptools import setup, find_packages

setup(
    name="devexp_sdk",
    version="0.1.0",
    description="A Python SDK for interacting with the devexp API",
    packages=find_packages(exclude=["tests*", "server*", "docs*", "openapi*"]),
    install_requires=[
        "requests>=2.28.0",
        "phonenumbers>=8.13.14",
        "pyyaml>=6.0",
        "Flask>=2.2.0",
    ],
    python_requires=">=3.7",  # Minimum Python version
)
