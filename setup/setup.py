from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import venv

ERROR_MSG = "Error occured while running command"
PRETTY_LINES = "*" * 80
VENV_NAME = ".venv"
VIRTUAL_ENV = "VIRTUAL_ENV"

SUBPROCESS_PARAMS = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.PIPE,
    "check": True,
}


def main() -> int:
    return_code_one = setup_environment()
    return 0 or return_code_one


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
    parent_dir = pathlib.Path(os.getcwd())
    python_venv_path = str(parent_dir / VENV_NAME)

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


if __name__ == "__main__":
    main()
