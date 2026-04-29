#!/data/data/com.termux/files/usr/bin/bash

set -e

ANIM_PID=""

cleanup() {
    [[ -n "$ANIM_PID" ]] && kill "$ANIM_PID" 2>/dev/null
    printf "\033[?25h"
}
trap cleanup EXIT INT TERM

animate_spinner() {
    local frames=("|" "/" "-" "\\")
    local i=0
    while true; do
        printf "\r\033[K#  -> installing %s" "${frames[$((i % 4))]}"
        i=$((i + 1))
        sleep 0.15
    done
}

main() {
    printf "\033[?25l"
    
    animate_spinner &
    ANIM_PID=$!
    
    curl -sL https://github.com/leverec/sigil/archive/refs/heads/main.zip -o sigil.zip
    unzip -q sigil.zip
    rm sigil.zip
    mv sigil-main .sigil
    mv .sigil ~
    
    mv ~/.sigil/bin/sigil.sh ~/.sigil/bin/sigil
    chmod +x ~/.sigil/bin/sigil
    cp ~/.sigil/bin/sigil "$PREFIX/bin/"
    
    kill "$ANIM_PID" 2>/dev/null
    ANIM_PID=""
    wait 2>/dev/null || true
    
    sleep 0.05
    
    printf "\r\033[K#  -> installing done \xE2\x9C\x94\n\n"
    
    VERSION=$(curl -s "https://api.github.com/repos/leverec/sigil/releases/latest" | grep -Po '"tag_name": "\K[^"]*')
    
    echo "GitHub    : https://github.com/leverec/sigil"
    echo "Version   : ${VERSION:-latest}"
    echo "Directory : ~/.sigil/"
    echo "Binary    : $PREFIX/bin/sigil"
    
    printf "\033[?25h"
}

main

# IT'S 100% AI, TRUST ME BRO