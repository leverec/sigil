#!/usr/bin/env bash

set -f
export SIGIL_HOME="$HOME/.sigil"
if [ ! -d "$SIGIL_HOME" ]; then
    echo -e "\033[31m--------- [ FATAL ERROR ] ---------"
    echo -e "Directory $SIGIL_HOME not found."
    echo -e ""
    echo -e "Try re-install sigil, the guidelines:"
    echo -e "https://github.com/leverec/sigil"
    echo -e ""
    echo -e "Installation:"
    echo -e "- run the script installer: ./installer.sh"
    echo -e "- or manually copy the source directory to $SIGIL_HOME"
    echo -e "-----------------------------------\033[0m"
    exit 1
else
    export PYTHONPATH="$SIGIL_HOME/src:$PYTHONPATH"
    python3 "$SIGIL_HOME/src/main.py" "$@"
fi
set +f