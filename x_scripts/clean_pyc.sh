#!/bin/bash

# clean pyc and orig files
rm -rf __pycache__

find repositories | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find repositories -type d -empty | awk '{print "remove empty folder "$0;system("rm -rf "$0)}'
