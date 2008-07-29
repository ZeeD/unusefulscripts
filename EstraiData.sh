#!/bin/sh

echo "TODO: cercare di farne una versione python" >&2

if [ -z "${1}" ]; then
    echo "Uso: ${0} IMMAGINE [IMMAGINI]" >&2
    echo "Rinomina ogni immagine con la propria timestamp" >&2
fi

if ! check_requirements.sh exiv2 grep cut mv; then
    exit -1
fi

for f in "${@}"; do
    mv "$f" "$(exiv2 "$f" | grep timestamp | cut -c19-37).${f#*.}"
done
