#!/bin/bash
#
# Use curl to make some HTTP requests to our flask endpoint
#

# Globals

if [[ "$#" -eq 1 ]]; then
    url=$1
else
    url=http://localhost:8080/
fi

echo "url is set to: $url"

_tests_run=0
_tests_failed=0
trap do_exit EXIT

function do_test(){
    # Runs a command, warning on non-zero exit
    # $* should contain argv with quotes escaped as necessary

    command=$*
    echo "======================"
    echo "Running test $[ $_tests_run +1 ]: $command"
    echo "======================"

    sh -c "$command"
    rc=$?
    echo -e "\n\n"

    (( _tests_run++ ))
    if [[ $rc -ne 0 ]]; then
        echo "WARNING: Command returned non-zero value: $rc" >&2
        (( _tests_failed++ ))
    fi
}

function do_exit(){
    # Function called upon exit

    echo "*** $_tests_run tests run, $_tests_failed returned non-zero ***"
    [[ $_tests_failed -ne 0 ]] && exit 1
}

# Basic get test
do_test curl -v $url

# Get tests with 'Accept' header set
for header in 'text/html' 'application/json'; do
    do_test curl -v -H \"Accept: ${header}\" $url
done

# POST method testing (foo)
# use a heredoc to simplify quoting
read -d '' data <<EOF
'{"foo": "This is a foo test from curl"}'
EOF
do_test curl -v -H \"Content-Type: application/json\" -d "$data" $url

# POST method testing (bar)
# use a heredoc to simplify quoting
read -d '' data <<EOF
'{"bar": "This is a bar test from curl"}'
EOF
do_test curl -v -H \"Content-Type: application/json\" -d "$data" $url



