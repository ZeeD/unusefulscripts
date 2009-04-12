#!/bin/bash

grep -i "^%folder/${@}" <<< '%folder/Album/%artist/%year - %album - %discnumber/%track - %title.%type
%folder/Compilation/%year - %album - %discnumber/%track - %artist - %title.%type'

