#!/bin/sh

# 2008-07-29 - Introduzione di check_requirements.sh
# 2008-06-03 - Piccole modifiche:
#   * formula a tutta pagina ($$_$$ invece che $_$)
#   * sfondo bianco
#   * supporto di un nome di file di output
#   * TODO: ritaglio più accurato   ->  done
#   * TODO: supporto alle opzioni
#   * TODO: supporto automagico alla visualizzazione
#   * TODO: in questo caso, supporto automagico all'autodistruzione
# 2007-??-?? - Versione iniziale

if [ -z "${1}" -o -n "${3}" ]; then
    echo "Uso: ${0} FORMULA [NOMEFILE]" >&2
    exit 1
elif [ -e "${1}.png" ]; then
    echo "Error! '${1}.png' esistente!" >&2
    exit 2
fi

if ! check_requirements.sh pwd mktemp latex dvipng; then
    exit -1
fi

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
