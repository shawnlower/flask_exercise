#!/bin/bash
#
# Use curl to make some HTTP requests to our flask endpoint
#

# Globals

URL=http://localhost:5000/


echo "URL is set to: $URL"

function do_test(){
    # Runs a command, warning on non-zero exit
    # $* should contain argv with quotes escaped as necessary

    command=$*
    echo "======================"
    echo "Running test: $command"
    echo "======================"

    eval $command
    rc=$?
    echo -e "\n\n"

    if [[ $rc -ne 0 ]]; then
        echo "WARNING: Command returned non-zero value: $rc" >&2
        return 1
    fi
}

do_test curl -v $URL

for header in 'text/html' 'application/json'; do
    do_test curl -v -H \"Accept: ${header}\" $URL
done

