#!/bin/sh

function PackageSize {
    echo -n "$(basename ${1}): "

    sed -e '1,/^FILE LIST:$/d' -e 's_^_/_g' "${1}"              |
    xargs file                                                  |
    grep -v -e 'directory $' -e '(No such file or directory)$'  |
    cut -d: -f1                                                 |
    tr '\n' '\0'                                                |
    du -hc --files0-from -                                      |
    tail -1
}

function PackageSizes {
    for package in "${@}"; do
        PackageSize "${package}"
    done
}

PackageSizes "${@}"
