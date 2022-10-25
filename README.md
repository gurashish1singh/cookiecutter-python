# Cookiecutter Python Package

My take on a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package with Poetry as the dependency manager.

**NOTE:** Only Python3.8+ is supported.

---

## Features
- Hooks: Pre-commit
- Linters: Black, Flake8, Flake8-bugbear, Isort, and Lizard
- Testing Frameworks (Optional): Pytest, Coverage, and CovDefaults

## Usage

First install the `cookiecutter` library.

```py
python -m pip install cookiecutter
```

Create a new repository on Github and then navigate to the directory where you would want to clone the repository.
```py
python -m cookiecutter https://github.com/gurashish1singh/cookiecutter-python.git
```
