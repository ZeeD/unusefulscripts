#!/bin/sh

function check_requirements() {
    # Uso: check_requirements PROGRAMMA [PROGRAMMI]
    # Controlla che i parametri siano programmi eseguibili
    for requirement in "${@}"; do
        if ! which "${requirement}" >/dev/null 2>/dev/null; then
            echo "Error: ${requirement} non è disponibile sul tuo sistema" >&2
            exit -1
        fi
    done
}

function join_() {
    # Uso: join_ SEPARATOR [STRINGHE]
    # porting in bash di str.join del python
    separator="${1}"
    echo -n "${2}"
    shift 2
    for element in "${@}"; do
        echo -n "${separator}${element}"
    done
}

function in_() {
    # uso in_ [-q] SEARCHED_ELEMENT [ELEMENTS]
    # porting in bash della keyword in del python
    if [ "${1}" = '-q' ]; then
        QUIET=true
        searched_element="${2}"
        shift 2
    else
        QUIET=false
        searched_element="${1}"
        shift
    fi
    for element in "${@}"; do
        if [ "${searched_element}" = "${element}" ]; then
            if ! "${QUIET}"; then
                echo "${searched_element}"
            fi
            return 0
        fi
    done
    return 1
}
