#!/bin/bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

rm -r .venv

virtualenv .venv -p python3.11
.venv/bin/pip install -r requirements.txt

while [ "$#" -gt 0 ]; do
  set -e
  .venv/bin/pip install "$1"
  echo "$1" >> requirements.txt
  shift
done