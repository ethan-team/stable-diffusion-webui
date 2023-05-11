#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from x_scripts.xe_autodl_proxy import setup_proxy_env
from xe_run_core import build_args, prepare_environment, start


if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal"
    setup_proxy_env()
    build_args()
    prepare_environment()
    start()
