#!/bin/bash

set -e
errors=0

# Run unit tests
python3 rump/unit_test.py || {
    echo "'python python/rump/unit_test.py' failed"
    let errors+=1
}

# Check program style
python3 -m pylint -E rump/*.py || {
    echo 'pylint -E rump/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"
