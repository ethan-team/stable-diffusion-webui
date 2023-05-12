#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from x_scripts.xe_autodl_proxy import setup_autodl_proxy_env
from x_scripts.es_init_copy_fs_to_tmp import DataDirSetup
from x_scripts.es_init_setup_symlink_dirs import SymlinkDirsSetup
from x_hacked_launch import build_args, prepare_environment, start


if __name__ == "__main__":
    DataDirSetup.ensure_data_copied()
    SymlinkDirsSetup.ensure_working_dir()

    os.environ["LANUCH_MODE"] = "normal"
    setup_autodl_proxy_env()

    build_args(force_terminate_existing=True)
    prepare_environment()
    start()
