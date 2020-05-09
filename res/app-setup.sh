#!/bin/bash

die() {
    echo "ERROR: $1"
    exit 1
}

echo "Setting up Kivy dependencies..."
# Based on https://kivy.org/doc/stable/installation/installation-rpi.html,
# with change from python to python3 and added --upgrade
apt install --upgrade -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python3-dev libmtdev-dev \
   xclip xsel libjpeg-dev || die "Could not install Kivy dependencies"

echo "Installing libgphoto..."
apt install --upgrade -y libgphoto2-dev pkg-config || die "Could not install libgphoto"

# Only create and enter venv if we are not already inside one
[ -z "$VIRTUAL_ENV" ] && {
    echo "Setting up venv..."
    apt install --upgrade -y python3-venv || die "Could not install python3-venv"
    VENV_DIR=$(dirname $0)/../venv
    python3 -m venv $VENV_DIR || die "Could not create virtual environment"
    . $VENV_DIR/bin/activate || die "Could not enter virtual environment"
}

python -m pip install -r $(dirname $0)/requirements.txt || die "Could not install pip packages"

echo "Downloading fonts..."
python - << EOF
import kivysome
import os.path
kivysome.enable("https://kit.fontawesome.com/58bcf53674.js", font_folder=os.path.join(os.path.dirname(__file__), "venv", "lib", "fonts"))
EOF
[ $? == 0 ] || die "Could not download fonts"
