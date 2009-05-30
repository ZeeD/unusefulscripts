#!/bin/sh

source utilities.sh # check_requirements, in_

if [ -z "${*}" -o -n "$(in_ "${1}" '-h' '--help')" ]; then
    echo "Uso: ${0} [-h|-f] FORMULA [NOMEFILE]" >&2
    exit 1
fi
if in_ -q "${1}" '-f' '--force'; then
    FORCE=true
    shift 1
else
    FORCE=false
fi
if [ -n "${2}" ]; then
    OUTPUT_FILENAME="${2}"
else
    OUTPUT_FILENAME="${1}.png"
fi
if [ -e "${OUTPUT_FILENAME}" ]; then
    if "${FORCE}"; then
        echo "Warning! '${OUTPUT_FILENAME}' esistente!" >&2
    else
        echo "Warning! '${OUTPUT_FILENAME}' esistente!" >&2
        exit 2
    fi
fi

check_requirements pwd mktemp pdflatex pdfcrop pdftoppm convert

MYDIR="$(pwd)"
TMPDIR="$(mktemp -dt tex2png-XXXXXX)"
cd "${TMPDIR}"
cat <<TEXSOURCE | pdflatex >/dev/null
\documentclass{article}
\pagestyle{empty}
\usepackage{xspace,amssymb,amsfonts,amsmath,color}
\usepackage{mathptmx}
\begin{document}
\$\$${1}\$\$
\end{document}
TEXSOURCE
pdfcrop 'texput.pdf' 'crop.pdf' >/dev/null
pdftoppm -gray -freetype yes -aa yes -aaVector yes 'crop.pdf' 'image'
convert 'image-1.pgm' "${MYDIR}/${OUTPUT_FILENAME}"
rm -Rf "${TMPDIR}"
