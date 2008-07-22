#!/bin/sh

if [ -z "${1}" -o -n "${2}" ]; then
    echo "Uso: ${0} file.dot" >&2
    exit 1
fi

in="${1}"
out="$(mktemp -t dotdisplay-XXXXXX)"

if [ ! -e "${in}" ]; then
    echo "Error! ${in}: file not found" >&2
    exit 2
fi

dot -Tsvg -o "${out}" "${in}" && svgdisplay "${out}" >/dev/null && rm "${out}"
