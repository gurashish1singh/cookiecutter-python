# Cookiecutter Python Package

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) blank template for a project.

**NOTE:** Only Python 3.8+ is supported.

---

## Features
- Package manager: pip
- Formatters and Linters: Ruff
- Testing Frameworks (Optional): Pytest, Coverage, and CovDefaults

## Usage

- bash setup.sh

- This template uses post-project generation hooks to:
   - Initialize a git repository (with default branch as main), IF the working directory is not already a git repository.

     **NOTE**: You will have to create a repositry on remote if it doesn't already exist before running the cookiecutter command.
   - Create a python virtual environment and activate it
   - Install ruff
   - Include an initial lint github workflow
