#!/bin/sh

echo "TODO: cercare di farne una versione python" >&2

for f in "${@}"; do
    mv "$f" "$(exiv2 "$f"|grep timestamp|cut -c19-37).${f#*.}"
done
