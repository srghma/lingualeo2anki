#!/bin/bash

SCRIPT_DIR=`dirname "${BASH_SOURCE[0]}"`
export PYTHONPATH=$SCRIPT_DIR
python -m server "$@"
