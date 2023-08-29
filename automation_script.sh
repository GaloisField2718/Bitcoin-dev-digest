#!/bin/bash
cd ~/Bitcoin-dev-digest;
. /home/galois/.local/share/virtualenvs/Bitcoin-dev-digest-jQKfwVSv/bin/activate;
python3 script.py > ~/Bitcoin-dev-digest/logs/log.txt 2>&1;
