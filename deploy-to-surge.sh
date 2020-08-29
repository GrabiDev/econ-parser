#!/bin/sh
mkdir ./public
python3 econ-parser.py
echo -e "machine surge.surge.sh\n" >> $HOME/.netrc
echo -e "    login $SURGE_LOGIN\n" >> $HOME/.netrc
echo -e "    password $SURGE_TOKEN\n" >> $HOME/.netrc
surge public --domain $SURGE_DOMAIN