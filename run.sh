#!/usr/bin/bash

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python "$MY_DIR"/day_"$1".py
