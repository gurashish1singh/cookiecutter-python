from __future__ import annotations

import os
import pathlib
import shlex
import subprocess
import sys
import venv
from pathlib import Path

ERROR_MSG = "Error occured while running command"
PRETTY_LINES = "*" * 80
PROJECT_NAME = "{{ cookiecutter.project_slug }}"
# TODO: Can allow user to pass it in through cookiecutter.json
VENV_NAME = ".venv"
VIRTUAL_ENV = "VIRTUAL_ENV"


# Setting up environment
SUBPROCESS_PARAMS = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.PIPE,
    "check": True,
}


def main() -> int:
    working_dir = Path().resolve()
    git_dir = Path(working_dir, ".git")
    return_code_one = 0
    if not git_dir.exists():
        return_code_one = initialize_git()

    if return_code_one == 0:
        return_code_two = setup_environment()

    if return_code_two == 0:
        return_code_three = _rename_pyproject_toml_file()
        print(f"New project {PROJECT_NAME!r} is setup.")

    return 0 or return_code_one or return_code_two or return_code_three


def initialize_git() -> int:
    COMMANDS_AND_MESSAGE = {
        "default_branch": (
            shlex.split("git config --global init.defaultBranch main"),
            PRETTY_LINES,
        ),
        "init_git": (
            shlex.split("git init"),
            "Initializing an empty git repository locally. You will have to create a repository "
            "on remote.\n",
        ),
    }
    for cmds, message in COMMANDS_AND_MESSAGE.values():
        print(message)
        try:
            subprocess.run(cmds, **SUBPROCESS_PARAMS)
        except subprocess.CalledProcessError as e:
            print(ERROR_MSG, e)
            return e.returncode

    return 0


def setup_environment() -> int:
    return_code = 0
    try:
        # Always create a new environment in the project dir
        python_venv_path = _create_new_environment()
        system_type, python_executable_path, python_activate_script_path = _get_python_paths(venv_path=python_venv_path)
        _activate_environment(system_type, python_activate_script_path)
    except Exception:
        return_code = -1
    return_code = _install_requirements(python_executable_path)
    return 0 or return_code


def _create_new_environment() -> str:
    parent_dir = pathlib.Path(os.getcwd()).parent.resolve()
    project_name = PROJECT_NAME.strip()
    python_venv_path = str(parent_dir / project_name / VENV_NAME)

    print(PRETTY_LINES)
    print(f"Attempting to create a new virtual env at {python_venv_path}")
    try:
        venv.create(env_dir=python_venv_path, with_pip=True)
    except Exception:
        print("An unexpected error has occured")
        raise

    print(f"Successfully created virtualenv at: {python_venv_path!r}")
    return python_venv_path


def _get_python_paths(venv_path: str) -> tuple[str, str, str]:
    sys_type = sys.platform
    if sys_type == "win32":
        python_executable_path = pathlib.Path(venv_path, "Scripts", "python.exe")
        activate_script_path = pathlib.Path(venv_path, "Scripts", "activate")
    elif sys_type in ("darwin", "linux", "linux2"):
        python_executable_path = pathlib.Path(venv_path, "bin", "python")
        activate_script_path = pathlib.Path(venv_path, "bin", "activate")
    else:
        raise OSError(f"Unsupported platform: {sys_type!r}")
    return sys_type, str(python_executable_path), str(activate_script_path)


def _activate_environment(system_type: str, activate_script_path: str) -> None:
    if system_type == "win32":
        subprocess.call(["cmd.exe", "c", activate_script_path])
    elif system_type in ("darwin", "linux", "linux2"):
        subprocess.call(f"source {activate_script_path}", shell=True)

    print("Successfully activated virtualenv.")
    print(f"\n{PRETTY_LINES}")


def _install_requirements(python_executable_path: str) -> int:
    print("Installing all dependencies from the requirements.txt file.\n")
    try:
        subprocess.run(
            [python_executable_path, "-m", "pip", "install", "-r", "requirements.txt"],
            **SUBPROCESS_PARAMS,
        )
        if "{{ cookiecutter.project_slug }}":
            subprocess.run(
                [python_executable_path, "-m", "pip", "install", "-r", "dev-requirements.txt"],
                **SUBPROCESS_PARAMS,
            )
    except subprocess.CalledProcessError as e:
        print(ERROR_MSG, e)
        return e.returncode

    print(PRETTY_LINES)
    return 0


def _rename_pyproject_toml_file() -> int:
    try:
        os.rename(
            "template-pyproject.toml",
            "pyproject.toml",
        )
    except subprocess.CalledProcessError as e:
        print(ERROR_MSG, e)
        return e.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
