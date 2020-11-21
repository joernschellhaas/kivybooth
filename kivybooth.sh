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
rc=${PIPESTATUS[0]}

if [ $rc -ne 0 ] && [ $rc -ne 120 ] ; then # Check if we stopped unintentionally
    echo "Kivybooth failed (RC=${rc}). Will restart system in 30 seconds..."
    sleep 30 # Wait a little so that we have a little time to connect to the device in case of boot loops
    reboot
fi
