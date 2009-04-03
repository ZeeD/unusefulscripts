#!/bin/sh

# "${1}" == '--guess-here' | '' 
# "${2}" == URL

ark --extract-to ${1} "$(dirname "${2}")" "${2}" # ${1} non è quotata apposta!
