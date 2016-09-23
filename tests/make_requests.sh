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

    sh -c "$command"
    rc=$?
    echo -e "\n\n"

    if [[ $rc -ne 0 ]]; then
        echo "WARNING: Command returned non-zero value: $rc" >&2
        return 1
    fi
}

# Basic get test
do_test curl -v $URL

# Get tests with 'Accept' header set
for header in 'text/html' 'application/json'; do
    do_test curl -v -H \"Accept: ${header}\" $URL
done

# POST method testing (foo)
# use a heredoc to simplify quoting
read -d '' data <<EOF
'{"foo": "This is a foo test from cURL"}'
EOF
do_test curl -v -H "Content-Type: application/json" -d "$data" $URL

# POST method testing (bar)
# use a heredoc to simplify quoting
read -d '' data <<EOF
'{"bar": "This is a bar test from cURL"}'
EOF
do_test curl -v -H "Content-Type: application/json" -d "$data" $URL
