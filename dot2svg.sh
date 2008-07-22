#!/bin/sh

if [[ -z "${@}" ]]; then
    echo "Uso: ${0} [f] file.dot [files]" >&2
    exit 1
fi

if [[ "${1}" == "f" ]]; then
    force="1"
    shift
fi

for parametro in ${@}; do
    if [[ ! -e "${parametro}" ]]; then
        echo "Warn! ${parametro}: file not found" >&2
        continue
    fi
    if [[ "${force}" == "1" || ! -e "${parametro/dot/svg}" ]]; then
        dot -Tsvg -o "${parametro/dot/svg}" "${parametro}"
    else
        echo "Warn! ${parametro/dot/svg}: file already found" >&2
        continue
    fi
done
