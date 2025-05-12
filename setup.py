#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent.absolute()

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0",  # Core testing package
        "pytest-xdist",  # Multi-process runner
        "pytest-cov>=4.0.0,<5",  # Coverage analyzer plugin
        "pytest-mock",  # For creating mocks
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
        "hypothesis-jsonschema==0.19.0",  # JSON Schema fuzzer extension
        "eth-hash[pycryptodome]",  # For backends to work
    ],
    "lint": [
        "black>=25.1.0,<26",  # Auto-formatter and linter
        "mypy>=1.15.0,<2",  # Static type analyzer
        "types-setuptools",  # Needed for mypy type shed
        "flake8>=7.2.0,<8",  # Style linter
        "flake8-breakpoint>=1.1.0,<2",  # Detect breakpoints left in code
        "flake8-print>=5.0.0,<6",  # Detect print statements left in code
        "flake8-pydantic",  # For detecting issues with Pydantic models
        "flake8-type-checking",  # Detect imports to move in/out of type-checking blocks
        "isort>=6.0.1,<7",  # Import sorting linter
        "mdformat>=0.7.22",  # Auto-formatter for markdown
        "mdformat-gfm>=0.3.5",  # Needed for formatting GitHub-flavored markdown
        "mdformat-frontmatter>=0.4.1",  # Needed for frontmatters-style headers in issue templates
        "mdformat-pyproject>=0.0.2",  # Allows configuring in pyproject.toml
    ],
    "doc": ["sphinx-ape"],
    "release": [  # `release` GitHub Action job uses this
        "setuptools>=75.6.0",  # Installation tool
        "wheel",  # Packaging tool
        "twine==3.8.0",  # Package upload tool
        "packaging>=23.1,<24",  # Needed for twine
    ],
    "dev": [
        # commitizen: Manage commits and publishing releases
        (here / "cz-requirement.txt").read_text().strip(),
        "pre-commit",  # Ensure that linters are run prior to committing
        "pytest-watch",  # `ptw` test watcher/runner
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["doc"]
    + extras_require["release"]
    + extras_require["dev"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="eth-pydantic-types",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="eth-pydantic-types: Pydantic Types for Ethereum",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ApeWorX Ltd.",
    author_email="admin@apeworx.io",
    url="https://github.com/ApeWorX/eth-pydantic-types",
    include_package_data=True,
    install_requires=[
        "cchecksum>=0.0.3,<1",
        "hexbytes>=0.3.1,<2",
        "eth-utils>=2.3.1,<6",
        "eth-typing>=3.5.2,<6",
        "pydantic>=2.5.2,<3",
        "typing_extensions>=4.8.0,<5",
    ],
    python_requires=">=3.9,<4",
    extras_require=extras_require,
    py_modules=["eth_pydantic_types"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"eth_pydantic_types": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
