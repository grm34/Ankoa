#!/bin/bash
pacman --noconfirm -Sy git python-pip unzip
wget https://raw.githubusercontent.com/grm34/AnkoA/master/PyArchboot.zip
unzip PyArchboot.zip  && rm PyArchboot.zip
# git clone https://github.com/grm34/PyArchboot.git
pip install -r ~/PyArchboot/requirements.txt
echo "alias PyArchboot='cd PyArchboot && python PyArchboot.py'" >> ~/.zshrc
# shellcheck source=/dev/null
source ~/.zshrc
