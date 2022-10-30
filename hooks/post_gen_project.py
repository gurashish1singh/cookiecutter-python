#!/usr/bin/env python
from pathlib import Path
import shlex
import subprocess
import sys

ERROR_MSG = "Error occured while running cmd"
PRETTY_LINES = "*" * 80


def main() -> int:
    working_dir = Path().resolve()
    git_dir = Path(working_dir, ".git")
    ret_code_one = 0
    if not git_dir.exists():
        ret_code_one = initialize_git()

    if ret_code_one == 0:
        ret_code_two = setup_environment()
    return ret_code_one or ret_code_two or 0


def initialize_git() -> int:
    COMMANDS_AND_STATUS = {
        "default_branch": (
            shlex.split("git config --global init.defaultBranch main"),
            PRETTY_LINES
        ),
        "init_git": (
            shlex.split("git init"),
            "Initializing an empty git repository\n"
        ),
    }
    for cmds, message in COMMANDS_AND_STATUS.values():
        print(message)
        try:
            subprocess.run(
                cmds,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(ERROR_MSG, e)
            return e.returncode

    return 0


def setup_environment() -> int:

    COMMANDS_AND_STATUS = {
        "install_poetry": (
            shlex.split("poetry install"),
            f"\n{PRETTY_LINES}\nInstalling poetry virtual environment"
        ),
        "install_pre_commit": (
            shlex.split(
                "poetry run pre-commit install --hook-type pre-commit --hook-type pre-push"
            ),
            f"\n{PRETTY_LINES}\nInstalling pre-commit hooks"
        )
    }
    for cmds, message in COMMANDS_AND_STATUS.values():
        print(message)
        try:
            subprocess.run(
                cmds,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(ERROR_MSG, e)
            return e.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
