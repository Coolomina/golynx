#!/bin/bash

TOTAL_REQUESTS=1000000

generate_random_string() {
    local length=$1
    # Generate a random string of specified length
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w "$length" | head -n 1
}

make_request() {
    URL="http://localhost:8000/api/golink"
    local link=$(generate_random_string 10)
    local redirection=$(generate_random_string 15)
    local payload="{\"link\": \"$link\", \"redirection\": \"$redirection\"}"
    curl -X PUT -H "Content-Type: application/json" -d "$payload" "$URL"
}

export -f make_request
export -f generate_random_string

seq $TOTAL_REQUESTS | xargs -n1 -P100 -I{} bash -c 'make_request'