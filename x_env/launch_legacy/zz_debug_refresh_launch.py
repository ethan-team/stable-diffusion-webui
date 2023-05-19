#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from xe_hack.xe_capture_output import resume_capture_all
from x_hacked_launch import build_args, prepare_environment, start

def _setup_proxy():
    from xe_hack.xe_autodl_proxy import setup_autodl_proxy_env
    setup_autodl_proxy_env()


if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "refresh:debug"
    
    resume_capture_all()
    _setup_proxy()

    build_args()
    prepare_environment()
    start()
