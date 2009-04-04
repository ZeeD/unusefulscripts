#!/bin/sh

source utilities.sh # check_requirements

if [ -z "${@}" ]; then
    echo "Uso: ${0} [f] file.dot [files]" >&2
    exit 1
fi

check_requirements dot

if [ "${1}" == "f" ]; then
    force="1"
    shift
fi

for parametro in ${@}; do
    if [ ! -e "${parametro}" ]; then
        echo "Warn! ${parametro}: file not found" >&2
        continue
    fi
    if [ "${force}" == "1" -o ! -e "${parametro/dot/ps}" ]; then
        dot -Tps -o "${parametro/dot/ps}" "${parametro}"
    else
        echo "Warn! ${parametro/dot/ps}: file already found" >&2
        continue
    fi
done
