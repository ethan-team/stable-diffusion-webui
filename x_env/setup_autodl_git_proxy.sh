#/bin/bash

echo "$AutoDLRegion"
if echo "$AutoDLRegion" | grep -q "neimeng"; then
    echo "export http_proxy=http://192.168.1.174:12798 && export https_proxy=http://192.168.1.174:12798"
    export http_proxy=http://192.168.1.174:12798 && export https_proxy=http://192.168.1.174:12798
else
    if echo "$AutoDLRegion" | grep -q "suqian"; then
        echo "http_proxy=http://10.0.0.7:12798 && export https_proxy=http://10.0.0.7:12798"
        export http_proxy=http://10.0.0.7:12798 && export https_proxy=http://10.0.0.7:12798
    else
        echo 'no http_proxy setup'
    fi
fi