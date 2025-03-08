#!/bin/bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd project

../.venv/bin/python3 manage.py "$@" --settings project.settings