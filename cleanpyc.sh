#!/bin/sh
find . -name '*pyc' -type f -print -exec rm -rf {} \;
