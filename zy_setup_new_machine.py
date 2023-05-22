#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def _setup_data_and_symlinks():
    from x_scripts.es_init_copy_fs_to_tmp import DataDirSetup
    from x_scripts.es_init_setup_symlink_dirs import SymlinkDirsSetup

    DataDirSetup.ensure_data_copied()
    SymlinkDirsSetup.ensure_working_dir()


if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal:debug"

    _setup_data_and_symlinks()

