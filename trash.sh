#!/bin/sh

source utilities.sh # in_, check_requirements

check_requirements kde-mv # kde-mv

if [ -z "${*}" -o -n "$(in_ "${1}" '-h' '--help')" ]; then
    echo "Uso: $0 [OPZIONE] [FILES]" >&2
    echo "butta FILES nel cestino." >&2
    echo "OPZIONE può essere una delle seguenti:" >&2
    echo "  -i: interattivo (chiedi conferma)" >&2
    echo "  -h|--help: mostra questa schermata" >&2
    exit -1
fi

if [ "${1}" = '-i' ]; then
    shift
    for filename in "${@}"; do
        read -e -n 1 -p "$0: rimuovere regular file \`${filename}'? " -s RISPOSTA
        if [[ "${RISPOSTA}" = [yYsS] ]]; then
            kde-mv "${filename}" 'trash:/'
        fi
    done
else
    kde-mv "${@}" 'trash:/'
fi

