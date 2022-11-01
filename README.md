# Cookiecutter Python Package

My take on a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package with Poetry as the dependency manager.

**NOTE:** Only Python 3.8+ is supported.

---

## Features
- Hooks: Pre-commit
- Formatters and Linters: Black, Flake8, Flake8-bugbear, Isort, and Lizard
- Testing Frameworks (Optional): Pytest, Coverage, and CovDefaults

## Usage

- Since this template uses Poetry as the dependancy manager, install poetry from `https://python-poetry.org/docs/#installation`

- Install the `cookiecutter` library.

    ```python
    python -m pip install cookiecutter
    ```

- Run the command:
    ```python
    python -m cookiecutter https://github.com/gurashish1singh/cookiecutter-python.git
    ```
- This template uses post-project generation hooks to:
   - Initialize a git repository (with default branch as main), IF the working directory is not already a git repository
   - Create a Poetry virtualenv
   - Install all dependencies
   - Install the pre-commit and pre-push hooks.
