#!/bin/bash
source x_script/setup_autodl_git_proxy.sh
git fetch --tag hooked
git checkout main
git pull hooked main
