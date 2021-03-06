#!/bin/sh

function cp1252_to_utf8() {
    TMP=/tmp
    ORIG="${TMP}/orig"
    STEP1="${TMP}/step1"
    STEP2="${TMP}/step2"

    mkdir -p "${ORIG}" "${STEP1}" "${STEP2}"
    for f in "${@}"; do
        mv "$f" "${ORIG}/$f";
        tr -d '\r' < "${ORIG}/$f" > "${STEP1}/$f"
        iconv --verbose -f CP1252 -t utf-8 -o "${STEP2}/$f" "${STEP1}/$f"
        cp "${STEP2}/$f" "$f"
    done
}

cp1252_to_utf8 "${@}"
