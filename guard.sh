#!/bin/bash

export PYTHONPATH="$(pwd)"

watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='python -m unittest'
