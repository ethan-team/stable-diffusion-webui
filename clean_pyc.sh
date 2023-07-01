#!/bin/bash

# clean pyc and orig files
find . | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
find . | grep '\.orig$' | awk '{print "remove "$0;system("rm -f "$0)}'
find . -type d -empty | awk '{print "remove empty folder "$0}'
find . -type d -empty -print0 | xargs -0 -I {} /bin/rmdir "{}"


# find repositories | grep '\.pyc$' | awk '{print "remove "$0;system("rm -f "$0)}'
# find repositories | grep '\.orig$' | awk '{print "remove "$0;system("rm -f "$0)}'
# find repositories -type d -empty | awk '{print "remove empty folder "$0}'
# find repositories -type d -empty -print0 | xargs -0 -I {} /bin/rmdir "{}"

