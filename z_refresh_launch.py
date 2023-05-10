#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from xe_run_core import build_args, prepare_environment, start
#from x_scripts.init_autodl_proxy import setup_proxy_env

if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "refresh::debug"
    #setup_proxy_env()
    build_args()
    prepare_environment()
    start()
