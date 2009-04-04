#!/bin/sh

source utilities.sh # join_, in_, check_requirements

allowed=(dot neato twopi circo fdp)

DOT="$(in_ "${2}" "${allowed[@]}")"
if [ -z "${1}" -o -n "${3}" -o \( -n "${2}" -a -z "${DOT}" \) ]; then
    echo "Uso: ${0} file.dot [$(join_ \| "${allowed[@]}")]"  >&2
    exit 1
fi

if [ -z "${DOT}" ]; then
    DOT=dot
fi

check_requirements "${DOT}" svgdisplay

if [ ! -e "${1}" ]; then
    echo "Error! ${1}: file not found" >&2
    exit 2
fi

out="$(mktemp -t dotdisplay-XXXXXX)"
"${DOT}" -Tsvg -o "${out}" "${1}" && svgdisplay "${out}" >/dev/null
rm "${out}"

