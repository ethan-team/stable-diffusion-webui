#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from x_hacked_launch import build_args, prepare_environment, start

def _setup_proxy():
    from x_scripts.xe_autodl_proxy import setup_autodl_proxy_env
    setup_autodl_proxy_env()

def _setup_data_and_symlinks():
    from x_scripts.es_init_copy_fs_to_tmp import DataDirSetup
    from x_scripts.es_init_setup_symlink_dirs import SymlinkDirsSetup

    DataDirSetup.ensure_data_copied()
    SymlinkDirsSetup.ensure_working_dir()


if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal:debug"

    _setup_data_and_symlinks()
    _setup_proxy()

    build_args(force_terminate_existing=True)
    prepare_environment()
    start()
