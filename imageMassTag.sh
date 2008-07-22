#!/bin/sh

function testRequiredPrograms() {
    for required in exiv2; do
        if ! which "${required}" >/dev/null 2>&1; then
            echo "Error: '${required}' is not installed on your system" >&2
            exit 2
        fi
    done
}

function main() {
    for directory in "${@}"; do
        echo "${directory}"
        # TODO: cattura la data dal nome della directory in (esempio) DATA
        # TODO: for immagine in directory/*; do
        # TODO:     cattura/calcola l'ora dell' immagine in ORA
        # TODO:     # exiv2 rm $IMMAGINE
        # TODO:     # exiv2 mo -M'add Exif.Photo.DateTimeOriginal "${DATA} ${ORA}"' ${IMMAGINE}
        # TODO:     # exiv2 mv -T ${IMMAGINE}
        # TODO: done
    done
}

function cellulareTonio() {
    # funzione speciale per le foto fatte col cellulare di antonio.
    # ha come parametri le directory su cui lavorare
    for directory in "${@}"; do
        for immagine in "${directory}/"*; do
            DATA="$(exiv2 -pc "${immagine}"|head -3|tail -1|sed 's|\([0-9]\+\)/\([0-9]\+\)/\([0-9]\+\)|\3:\2:\1|g')"
            ORA="$(exiv2 -pc "${immagine}"|head -4|tail -1)"
            exiv2 rm -d a "${immagine}"
            exiv2 mo -M"add Exif.Photo.DateTimeOriginal ${DATA} ${ORA}" "${immagine}"
            exiv2 mv -T "${immagine}"
        done
    done
}

testRequiredPrograms
# main "${@}"
cellulareTonio "${@}"
