#!/bin/bash

echo "$1"
source $VIRTUAL_ENV/bin/activate && pip3 install -e /private_modules/elemental.tools && python3 -m elemental_tools.Jarvis.install && python3 -m "$1"