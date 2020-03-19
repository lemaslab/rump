#!/bin/bash

set -e
errors=0

# Run unit tests
python rump/unit_tests.py || {
    echo "'python python/bionitio/bionitio_test.py' failed"
    let errors+=1
}

# Check program style
pylint -E rump/*.py || {
    echo 'pylint -E rump/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"
