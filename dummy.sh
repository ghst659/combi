#!/bin/bash

function main() {
    local word
    for word in "$@"; do
	# echo "${word}" >/dev/stderr
	if [[ "${word}" == "dirac:e3.1415" ]]; then
	    return 0
	fi
    done
    return 1
}

exit $(main "$@")
