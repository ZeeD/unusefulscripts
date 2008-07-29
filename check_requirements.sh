#!/bin/sh

if [ -z "${1}" ]; then
    echo "Uso: ${0} PROGRAMMA [PROGRAMMI]" >&2
    echo "Controlla che i parametri siano programmi eseguibili" >&2
fi

for requirement in "${@}"; do
    if ! which "${requirement}" >/dev/null 2>/dev/null; then
        echo "Error: ${requirement} non è disponibile sul tuo sistema" >&2
        exit -1
    fi
done
