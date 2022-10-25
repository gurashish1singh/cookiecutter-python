#!/bin/bash
set -eou pipefail

PRETTY_LINES=$(printf "=%.0s" {1..80})

msg()
{
    echo "$PRETTY_LINES"
    echo "$1"
    echo "$PRETTY_LINES"
}

setup_poetry()
{
    echo "Checking if poetry is already installed on the system"
    if [[ $(command -v poetry) ]]; then
        echo -e "Poetry is already installed on the system\n"
    else
        echo "Poetry is not installed."
        echo -e "Installing poetry from https://python-poetry.org/docs/ \n"
        curl -sSL https://install.python-poetry.org | python -
    fi

    msg "Installing poetry environment based on the template pyproject.toml file"
    poetry add \
        black@^22.9 \
        flake8@^5 \
        isort@^5.5 \
        pre-commit@^2.20 \
        --dev
    poetry add python-json-logger@^2 \
        pyyaml@^6
    poetry install
    echo
}

install_hooks()
{
    msg "Installing pre-commit hooks."
    poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
    echo
}

msg "Starting project setup"
setup_poetry
install_hooks
msg "Local setup completed!"
