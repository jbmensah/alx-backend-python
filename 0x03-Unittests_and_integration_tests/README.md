# Unit and Integration Testing Project

This repository contains utility functions and a GitHub organization client in Python, along with comprehensive unit and integration tests. It is designed to guide you through writing and running tests for Python applications.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Setup and Installation](#setup-and-installation)
4. [Available Scripts](#available-scripts)
5. [File Descriptions](#file-descriptions)
6. [Running Tests](#running-tests)
7. [Milestones](#milestones)
8. [Contributing](#contributing)

## Project Structure

```
your-repo/
│
├── venv/                   # Python virtual environment (ignore in version control)
│
├── utils.py                # Utility functions: access_nested_map, get_json, memoize
├── client.py               # GitHubOrgClient implementation
│
├── tests/                  # All test files
│   ├── __init__.py         # Makes tests/ a package
│   ├── fixtures.py         # JSON fixtures for integration tests
│   ├── test_utils.py       # Unit tests for utils.py (Milestones 0, 1, 2)
│   ├── test_client.py      # Unit tests for client.py (Milestones 3, 4, 5, 6)
│   └── integration/        # Integration tests
│       ├── __init__.py
│       └── test_public_repos.py  # Integration tests for public_repos (Milestone 7)
│
├── README.md               # Project documentation (this file)
└── requirements.txt        # Pip dependencies (parameterized, requests, etc.)
```

## Prerequisites

- **Python 3.6 or newer**  
- **pip** (Python package installer)  
- **Git** (optional, for cloning the repository)  
- **Windows Subsystem for Linux (WSL)** or any Unix-like shell  
- **Visual Studio Code** (or your preferred IDE)

## Setup and Installation

1. **Clone the repository** (if you haven’t already):
   ```bash
   git clone <your-repo-url>
   cd your-repo
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation** (optional):
   ```bash
   pip list
   ```

## Available Scripts

- **Run all tests**:
  ```bash
  python -m unittest discover -v
  ```
- **Run a specific test file**:
  ```bash
  python -m unittest tests/test_utils.py -v
  ```

## File Descriptions

- **utils.py**:  
  - `access_nested_map(nested_map, path)`: Accesses nested dictionaries by following a tuple of keys.  
  - `get_json(url)`: Sends an HTTP GET request, raises on non-200 status, returns parsed JSON.  
  - `memoize(func)`: Decorator that caches a function’s return value.

- **client.py**:  
  - `GithubOrgClient`: A class for interacting with the GitHub REST API for organizations.  
    - `org(self)`: Fetches organization data via `get_json`.  
    - `_public_repos_url`: Read-only property returning the URL of the public repos endpoint.  
    - `public_repos(self, license=None)`: Returns a list of public repositories, optionally filtered by license.  
    - `@staticmethod has_license(repo, license_key)`: Checks if a repository has a specific license.

- **tests/**:  
  - **test_utils.py**: Unit tests for each function in `utils.py`.  
  - **test_client.py**: Unit tests for each method in `client.py`, using `unittest.mock` to patch external calls.  
  - **fixtures.py**: Contains static JSON dictionaries/lists to mock GitHub API responses.  
  - **integration/test_public_repos.py**: Integration tests for the `public_repos` method, using `@parameterized_class` and patched `requests.get`.

- **requirements.txt**:  
  - Lists project dependencies (e.g., `parameterized`, `requests`).

## Running Tests

1. Ensure your virtual environment is active:
   ```bash
   source venv/bin/activate
   ```

2. From the repository root, run:
   ```bash
   python -m unittest discover -v
   ```
   - The `-v` (verbose) flag provides detailed test output.

3. **To run a specific test file**, for example:
   ```bash
   python -m unittest tests/test_utils.py -v
   ```

## Milestones

The project follows a structured set of milestones to guide you through learning and practicing unit/integration testing:

1. **Milestone 0**: Parameterized tests for `access_nested_map` (done in `tests/test_utils.py`).  
2. **Milestone 1**: Mock HTTP calls in `get_json` and verify behavior (in `tests/test_utils.py`).  
3. **Milestone 2**: Test the `memoize` decorator by patching an underlying method (in `tests/test_utils.py`).  
4. **Milestone 3**: Decorator-style patches & parameterization for `GithubOrgClient.org` (in `tests/test_client.py`).  
5. **Milestone 4**: Mock the readonly property `_public_repos_url` and test it (in `tests/test_client.py`).  
6. **Milestone 5**: Patch both `_public_repos_url` and external JSON fetch in `public_repos` (in `tests/test_client.py`).  
7. **Milestone 6**: Parameterize and test the static method `has_license` (in `tests/test_client.py`).  
8. **Milestone 7**: Integration test suite for `public_repos` using `@parameterized_class` and patched `requests.get` (in `tests/integration/test_public_repos.py`).

## Contributing

1. **Fork the repository** and create a new branch for your feature or bugfix.  
2. Ensure you’re following the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.  
3. Write or update tests to cover your changes.  
4. Submit a pull request describing your changes and referencing any issues.

---

Happy testing! 🚀
