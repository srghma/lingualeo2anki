#!/bin/bash
echo $@
python -m server "$@"
echo "done"
