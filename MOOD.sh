#!/bin/sh

# stupid wrapper around moodbar

find "$@" -type f -iregex '.*\.\(ogg\|mp3\|flac\|wma\)' -print0 | xargs -0 -n 1 -P 0 -- _MOOD_HELPER.sh
