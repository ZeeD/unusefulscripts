#!/bin/sh


function mp {
    for ext in '' 'avi' 'mkv' 'm4v'; do
        local fn="${1}${ext}"
        if [ -f "${fn}" ]; then
            mplayer "${fn}"
            break
        fi
    done
}

mp "${1}"
