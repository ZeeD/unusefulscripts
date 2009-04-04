#!/bin/sh

source utilities.sh # check_requirements

if [ -z "${1}" -o -n "${3}" ]; then
    echo "Uso: ${0} FORMULA [NOMEFILE]" >&2
    exit 1
elif [ -e "${1}.png" ]; then
    echo "Error! '${1}.png' esistente!" >&2
    exit 2
fi

check_requirements pwd mktemp latex dvipng

homeDir="$(pwd)"
cd "$(mktemp -dt tex2png-XXXXXX)"
echo '\documentclass{article}
\pagestyle{empty}
\usepackage{xspace,amssymb,amsfonts,amsmath,color}
\usepackage{mathptmx}
\begin{document}
$$'${1}'$$
\end{document}' > file.tex
latex file > /dev/null
dvipng -O -24.4cm,-6.6cm -D 300 -z 9 -o file.png file.dvi > /dev/null # -bg Transparent -O -9cm,-6cm
if [ -n "${2}" ]; then
    OUT="${homeDir}/${2}"
else
    OUT="${homeDir}/${1}.png"
fi
mv file.png "$OUT"
rm -R "$(pwd)"
