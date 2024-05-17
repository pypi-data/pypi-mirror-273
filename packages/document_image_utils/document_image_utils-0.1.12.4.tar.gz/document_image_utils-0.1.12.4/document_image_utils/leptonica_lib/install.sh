#!/usr/bin/env bash

# This script installs leptonica and tesseract from source
# it does not install other pre-requisites to a custom location.

# side note: install prefix is defined once per library.
# side note: it clones git repositories in the current directory.

set -e
set -u

# install leptonica
(
export INSTALL_PREFIX=~/.sources
git clone https://github.com/DanBloomberg/leptonica.git
mkdir leptonica/build ; cd leptonica/build
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX -DBUILD_PROG=1 ..
make -j8
make install
)