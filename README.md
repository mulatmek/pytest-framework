


# Framework

Short description
- Lightweight Python framework containing an API handler, cloud resource helpers, logging and report generation utilities.

## Prerequisites
- Python 3.12 (or compatible 3.x)
- `pip`
- Recommended: use the project virtual environment at `./.venv`

## Quick setup

1. Clone and open the project
   - `git clone <repo-url>`
   - `cd Framework`

2. Create and activate virtual environment
   - Create:
       
       python3 -m venv .venv
   - Activate:
       
       source .venv/bin/activate

3. Upgrade pip and install dependencies
       
       python -m pip install --upgrade pip
       python -m pip install -r requirements.txt

> Use `python -m pip` to ensure the `pip` tied to your virtual environment is used (avoids errors like `no such option: -m` if `pip` from a different Python is invoked).

## Running tests

- From project root with the venv activated:
    
    python -m pytest -q

- Run a single test file:
    
    python -m pytest tests/test_demo.py -q

If `pytest` appears missing even after installing, confirm the venv is active:
- `which python` should point to `.venv/bin/python`
- `which pytest` should point to `.venv/bin/pytest`  
Alternatively use `python -m pytest` to force use of the venv interpreter.



## Project structure (high level)
- `framework/` \- core code
  - `api_handler/` \- `api.py` (API handler)
  - `cloud_resources/` \- resource helpers (buckets, etc.)
  - `logging/` \- logger
  - `reporter/` \- report generator
  - `utils/` \- helpers
- `tests/` \- pytest tests
- `requirements.txt` \- pinned dependencies
- `Makefile`, `Dockerfile`, `entrypoint.sh`, `pytest.ini`

## `.gitignore` suggestion
Add a `.gitignore` file including:

    .venv/
    __pycache__/
    *.pyc
    .pytest_cache/
    .DS_Store
    .idea/

## Troubleshooting notes
- If `pytest` invoked from the wrong interpreter: prefer `python -m pytest`.
- If `make install` fails with `no such option: -m`, inspect the `Makefile` line that calls `pip` and change to `python -m pip install ...` (ensures the correct pip is used).
- If dependencies differ, re-run `python -m pip install -r requirements.txt` inside the activated venv.

## Contributing
- Open a PR on branchable feature/topic branches.
- Run tests locally before submitting.
- Follow code style and add unit tests for new features.

## License
- Add appropriate license file (e.g., `LICENSE`) and update this section.