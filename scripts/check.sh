#!/bin/bash
cd "$(dirname -- "$(dirname -- "$(readlink -f "$0")")")" || exit

for cmd in flake8 isort mypy pylint; do
    if [[ ! -x "$(which "$cmd")" ]]; then
        echo "Could not find $cmd. Please make sure that flake8, isort, mypy, and pylint are all installed."
        exit 1
    fi
done

flake8 shortener && isort --check shortener && mypy shortener && pylint shortener