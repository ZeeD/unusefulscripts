#!/bin/sh

output_format='ps'

source utilities.sh # check_requirements, in_

if [ -z "${*}" -o -n "$(in_ "${1}" '-h' '--help')" ]; then
    echo 'Uso: '"${0}"' [-f|-h] DOT_FILE [DOT_FILES]' >&2
    exit 1
fi

check_requirements dot

force='0'
if [ -n "$(in_ "${1}" '-f' '--force')" ]; then
    force='1'
    shift
fi

for dot_file in "${@}"; do
    if [ ! -e "${dot_file}" ]; then
        echo '[Warn] file not found: `'"${dot_file}"\' >&2
        continue
    fi
    output_file="${dot_file/dot/${output_format}}"
    if [ -e "${output_file}" -a "${force}" != '1' ]; then
        echo '[Warn] file found: `'"${output_file}"\'' (use -f to force)' >&2
        continue
    fi
    dot -T"${output_format}" -o "${output_file}" "${dot_file}"
done
