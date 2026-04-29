#!/data/data/com.termux/files/usr/bin/bash

set -e
trap 'printf "[!!] installation failed at line %s\n" "$LINENO" >&2' ERR

log()  { printf "[*] %s\n" "$*"; }
ok()   { printf "\033[92m[+] %s\n\033[0m" "$*"; }
err()  { printf "\033[31m[!] %s\n\033[0m" "$*" >&2; }
sep()  { printf "%.0s─" {1..45}; printf "\n"; }

main() {
    sep
    printf "     sigil installer\n"
    sep

    log "downloading archive from GitHub..."
    curl -L --progress-bar \
        https://github.com/leverec/sigil/archive/refs/heads/sigil.zip \
        -o sigil.zip
    ok "archive saved to: $(pwd)/sigil.zip"

    log "extracting sigil.zip..."
    DIR=$(unzip -Z1 sigil.zip | head -n1 | cut -d/ -f1)
    unzip -qo sigil.zip
    rm sigil.zip
    mv "$DIR" sigil-temp
    ok "extracted to: sigil-temp"

    if [[ -d ~/.sigil ]]; then
        printf "\033[33m[?] ~/.sigil already exists. overwrite? [y/N] \033[0m"
        read -r CONFIRM
        if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
            err "aborted by user"
            rm -rf sigil-temp
            exit 1
        fi
    fi

    log "installing to ~/.sigil/"
    rm -rf ~/.sigil
    mv sigil-temp ~/.sigil
    ok "installed"

    log "preparing binary..."
    mv ~/.sigil/bin/sigil.sh ~/.sigil/bin/sigil
    chmod +x ~/.sigil/bin/sigil
    cp ~/.sigil/bin/sigil "$PREFIX/bin/"
    ok "binary ready"

    log "fetching latest release tag..."
    VERSION=$(curl -s https://api.github.com/repos/leverec/sigil/releases/latest \
        | sed -n 's/.*"tag_name": "\([^"]*\)".*/\1/p')

    if [[ -z "$VERSION" ]]; then
        VERSION="unknown"
    fi

    sep
    printf "     install complete\n"
    sep
    printf "  github    : https://github.com/leverec/sigil\n"
    printf "  version   : %s\n" "$VERSION"
    printf "  directory : ~/.sigil/\n"
    printf "  binary    : %s/bin/sigil\n" "$PREFIX"
    sep
}

main