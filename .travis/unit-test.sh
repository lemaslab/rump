#!/bin/bash

set -e
errors=0

# Check program style
pylint -E src/*.py || {
    echo 'pylint -E bionitio/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"
