#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from xe_run_core import build_args, prepare_environment, start

def _setup_proxy():
    from x_scripts.init_autodl_proxy import setup_proxy_env
    setup_proxy_env()


if __name__ == "__main__":
    #os.environ["LANUCH_MODE"] = "refresh:debug:update_repo"
    os.environ["LANUCH_MODE"] = "refresh:debug"

    #_setup_proxy()

    build_args()
    prepare_environment()
    start()
