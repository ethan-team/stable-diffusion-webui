#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from x_scripts.xe_autodl_proxy import setup_proxy_env
from x_env.es_init_copy_fs_to_tmp import DataDirSetup
from x_env.es_init_setup_symlink_dirs import SymlinkDirsSetup
from xe_run_core import build_args, prepare_environment, start

if __name__ == "__main__":
    DataDirSetup.ensure_data_copied()
    SymlinkDirsSetup.ensure_working_dir()

    os.environ["LANUCH_MODE"] = "refresh"
    setup_proxy_env()
    build_args()
    prepare_environment()
    start()
