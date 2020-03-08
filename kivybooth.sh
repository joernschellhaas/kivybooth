#!/usr/bin/env bash

die() {
    echo "ERROR: $1"
    exit 1
}

# Only enter venv if we are not already inside one
[ -z "$VIRTUAL_ENV" ] && {
    VENV_DIR=$(dirname $0)/venv
    . $VENV_DIR/bin/activate || die "Could not enter virtual environment"
}

cd $(dirname $0)/venv/share/kivy-examples/demo/showcase
python main.py 2>&1 | grep --line-buffered '^\['
