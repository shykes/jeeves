#!/bin/bash

set -x

# Create virtualenv
virtualenv --no-site-packages ~/.env

./extend
