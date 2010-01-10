#!/bin/sh

source utilities.sh # in_

if [ -z "${*}" -o -n "$(in_ "${1}" '-h' '--help')" ]; then
    echo "Uso: $0 file1 file2 ">&2
    echo "Rinomina file1 in file2 e viceversa" >&2
    exit -1
fi

alias device='stat -c%d'

filea="${1}"
fileb="${2}"

if [ "$(device "${filea}")" != "$(device "$fileb")" ]; then
    echo "ERROR: i due file sono su due partizioni diverse!!"
    exit -2
fi

filet="$(mktemp --tmpdir="$(dirname "${filea}")")"

mv "${filea}" "${filet}"
mv "${fileb}" "${filea}"
mv "${filet}" "${fileb}"

