#!/data/data/com.termux/files/usr/bin/bash

set -e


log()  { printf "[  ] %s\n" "$*"; }
ok()   { printf "[OK] %s\n" "$*"; }
err()  { printf "[!!] %s\n" "$*" >&2; }
sep()  { printf "%.0s─" {1..45}; printf "\n"; }

main() {
    sep
    printf "     sigil installer\n"
    sep

    # download
    log "downloading archive from GitHub..."
    log "url : https://github.com/leverec/sigil/main.zip"
    curl -L --progress-bar \
        https://github.com/leverec/sigil/archive/refs/heads/main.zip \
        -o sigil.zip
    ok "archive saved to: $(pwd)/sigil.zip"

    # extract
    log "extracting sigil.zip..."
    unzip sigil.zip
    rm sigil.zip
    ok "extracted. removed sigil.zip"

    # move into place
    log "moving sigil-main/ -> ~/.sigil/"
    mv sigil-main ~/.sigil
    ok "installed to: $HOME/.sigil/"

    # binary setup
    log "renaming sigil.sh -> sigil"
    mv ~/.sigil/bin/sigil.sh ~/.sigil/bin/sigil
    ok "renamed"

    log "setting execute permission on binary..."
    chmod +x ~/.sigil/bin/sigil
    ok "chmod +x done"

    log "copying binary to \$PREFIX/bin/ ($PREFIX/bin/)..."
    cp ~/.sigil/bin/sigil "$PREFIX/bin/"
    ok "binary available at: $PREFIX/bin/sigil"

    # version check
    log "fetching latest release tag from GitHub API..."
    VERSION=$(curl -s "https://api.github.com/repos/leverec/sigil/releases/latest" \
        | grep -Po '"tag_name": "\K[^"]*')

    if [[ -z "$VERSION" ]]; then
        err "could not resolve version from GitHub API (no releases?)"
        VERSION="unknown"
    else
        ok "resolved version: $VERSION"
    fi

    # summary
    sep
    printf "     install complete\n"
    sep
    printf "  github    : https://github.com/leverec/sigil\n"
    printf "  version   : %s\n"   "${VERSION}"
    printf "  directory : ~/.sigil/\n"
    printf "  binary    : %s/bin/sigil\n" "$PREFIX"
    sep
}

main