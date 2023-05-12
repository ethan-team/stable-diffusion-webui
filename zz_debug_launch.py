#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from x_scripts.xe_autodl_proxy import setup_autodl_proxy_env
from x_scripts.xe_capture_output import resume_capture_all
from x_hacked_launch import build_args, prepare_environment, start

if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal:debug"
    resume_capture_all()
    setup_autodl_proxy_env()
    build_args()
    prepare_environment()
    start()
