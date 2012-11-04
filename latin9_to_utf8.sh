#!/bin/sh

function latin1_to_utf8() {
    mkdir 'orig' 'step1' 'step2'
    for f in "${@}"; do
        mv "$f" "orig/$f";
        tr -d '\r' < "orig/$f" > "step1/$f"
        iconv --verbose -f iso-8859-15 -t utf-8 -o "step2/$f" "step1/$f"
        cp "step2/$f" "$f"
    done
}

latin1_to_utf8 "${@}"
