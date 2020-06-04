#!/bin/bash

# Update pacman cache and install dependencies
pacman --noconfirm -Sy git python-pip unzip

# Clone the repository
wget https://raw.githubusercontent.com/grm34/AnkoA/master/PyArchboot.zip
unzip PyArchboot.zip  && rm PyArchboot.zip
# git clone https://github.com/grm34/PyArchboot.git

# Install requirements
pip install -r PyArchboot/requirements.txt

# Create an alias
echo "alias PyArchboot='cd PyArchboot && python PyArchboot.py'" >> /root/.zshrc
# shellcheck source=/dev/null
source /root/.zshrc
