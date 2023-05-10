#!/bin/bash

# clean pyc and orig files
rm -rf __pycache__

find modules | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find modules -type d -empty | awk '{print "remove empty folder "$0;system("rm -rf "$0)}'

find models | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find models -type d -empty | awk '{print "remove empty folder "$0;system("rm -rf "$0)}'

find repositories | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find repositories -type d -empty | awk '{print "remove empty folder "$0;system("rm -rf "$0)}'

find extensions | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find extensions -type d -empty | awk '{print "remove empty folder "$0;system("rm -rf "$0)}'

find extensions-builtin | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find extensions-builtin -type d -empty | awk '{print "remove empty folder "$0;system("rm -rf "$0)}'

