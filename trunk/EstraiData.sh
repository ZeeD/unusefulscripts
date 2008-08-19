#!/bin/sh

echo "TODO: cercare di farne una versione python" >&2

if [ -z "${1}" ]; then
    echo "Uso: ${0} IMMAGINE [IMMAGINI]" >&2
    echo "Rinomina ogni immagine con la propria timestamp" >&2
fi

if ! check_requirements.sh exiv2 grep cut mv; then
    exit -1
fi

for from in "${@}"; do
    timestamp="$(exiv2 "$from" 2>/dev/null | grep timestamp | cut -c19-37)"
    if [ -z "${timestamp}" ]; then
        echo "Errore: formato file non supportato" >&2
        exit -2
    fi
    to="${timestamp}.${from#*.}"
    if [ -e "${to}" ]; then
        echo "Errore: ${to} già presente" >&2
        exit -3
    fi
    mv -i "${from}" "${to}"
done
