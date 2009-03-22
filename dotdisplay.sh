#!/bin/sh

allowed=(dot neato twopi circo fdp)

function join_() {
    separator="${1}"
    echo -n "${2}"
    shift 2
    for element in "${@}"; do
        echo -n "${separator}${element}"
    done
}

function in_() {
    searched_element="${1}"
    shift
    for element in "${@}"; do
        if [ "${searched_element}" = "${element}" ]; then
            echo "${searched_element}"
            break
        fi
    done
}

DOT="$(in_ "${2}" "${allowed[@]}")"
if [ -z "${1}" -o -n "${3}" -o \( -n "${2}" -a -z "${DOT}" \) ]; then
    echo "Uso: ${0} file.dot [$(join_ \| "${allowed[@]}")]"  >&2
    exit 1
fi

if [ -z "${DOT}" ]; then
    DOT=dot
fi

if [ ! -e "${1}" ]; then
    echo "Error! ${1}: file not found" >&2
    exit 2
fi

out="$(mktemp -t dotdisplay-XXXXXX)"
"${DOT}" -Tsvg -o "${out}" "${1}" && svgdisplay "${out}" >/dev/null
rm "${out}"
