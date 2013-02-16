#!/bin/sh

function cp1252_to_utf8() {
    mkdir 'orig' 'step1' 'step2'
    for f in "${@}"; do
        mv "$f" "orig/$f";
        tr -d '\r' < "orig/$f" > "step1/$f"
        iconv --verbose -f CP1252 -t utf-8 -o "step2/$f" "step1/$f"
        cp "step2/$f" "$f"
    done
}

cp1252_to_utf8 "${@}"
