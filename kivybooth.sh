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

cd $(dirname $0)
python main.py 2>&1 | grep --line-buffered --invert-match '^INFO: The key you just pressed is not recognized by SDL\.'
