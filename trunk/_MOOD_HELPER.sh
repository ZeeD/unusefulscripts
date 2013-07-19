#!/bin/sh

# stupid helper for MOOD.sh

INFILE="${1}"
DIRNAME="$(dirname "${INFILE}")"
BASENAME="$(basename "${INFILE}")"
OUTFILE="${DIRNAME}/.${BASENAME%.*}.mood"

test -f "${OUTFILE}" || moodbar -o "${OUTFILE}" "${INFILE}"
