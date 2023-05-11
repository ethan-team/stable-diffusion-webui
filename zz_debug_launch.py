#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from x_scripts.xe_autodl_proxy import setup_proxy_env
from x_scripts.xe_environment import capture_sys_print
from xe_run_core import build_args, prepare_environment, start

if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal:debug"
    capture_sys_print()
    setup_proxy_env()
    build_args()
    prepare_environment()
    start()
