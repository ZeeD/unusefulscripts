#!/bin/sh
# 2007-01-04 - Versione 0.0.1 - Codename: "short circuit 1 : usability 0"

[ -n "${1}" ] || { echo "Uso: ${0} examples.prolog [...] [background.prolog [...]]" >&2; exit 1; }
tempfile="$(mktemp)" || { echo "Error: mktemp utility" >&2; exit 2; }
for f in "${@}"; do
    [ -f "${f}" ] || { echo "Warning: ${f} is not a file!" >&2; continue; }
    cat "${f}" >> "${tempfile}"
done
pl -sq "${tempfile}" || { echo "Error: pl -sq ${tempfile} utility" >&2; exit 4; }
rm "${tempfile}" || { echo "Error: rm utility (delete ${tempfile})" >&2; exit 5; }
