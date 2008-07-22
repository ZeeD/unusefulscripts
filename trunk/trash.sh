#!/bin/sh

[ -n "${*}" ] && kfmclient move "${@}" 'trash:/'
