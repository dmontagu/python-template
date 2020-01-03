New Python Project Template
===========================

A barebones cookiecutter template for creating new and modern python packages.

The generated project will have:
* Easy dependency management with `poetry` and `pyproject.toml`:
    * Recipe: `make lock`
        * Uses `poetry` to generate the `poetry.lock` dependency lockfile from `pyproject.toml` 
        * Also exports a `requirements.txt`, removing `poetry` as a requirement when deployed
* Fast set-up:
    * Recipe: `make develop`
        * Checks for presence of required commands (`python3`, `poetry`)
        * Uses `poetry` to create a properly configured virtual environment
* Lots of other useful Makefile recipes
    * `make format`: Auto-format with `isort`, `autoflake`, and `black`
    * `make lint`: Static analysis with `flake8`
    * `make mypy`: Type-check source and tests with `mypy`
    * `make test`: Execute tests with `pytest` and `coverage`
    * ... and more (run `make` or `make help` for more details) 


Usage
-----
```
cookiecutter git@github.com:dmontagu/python-template.git
```
