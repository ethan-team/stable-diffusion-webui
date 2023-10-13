#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import x_hacked_launch
from x_hacked_launch import build_args, init_pid, prepare_environment, start


def _setup_proxy():
    from xe_hack.xe_autodl_proxy import setup_autodl_proxy_env
    setup_autodl_proxy_env()

def _setup_data_and_symlinks():
    #from x_scripts.es_init_copy_fs_to_tmp import DataDirSetup
    from x_scripts.es_init_setup_symlink_dirs import SymlinkDirsSetup

    #DataDirSetup.ensure_data_copied()
    SymlinkDirsSetup.ensure_working_dir()

# 从server_conf.json读取配置，并设置环境变量
def _init_configs():
    os.environ["LAUNCH_MODE"] = "normal:debug"
    os.environ["LANGUAGE"] = "zh-cn"

    try:
        # 读取server-config.json，解析，保存在os.environ中
        with open('server-config.json', 'r') as f:
            import json
            configs = json.load(f)
            for k, v in configs.items():
                os.environ[k] = str(v)
    except Exception as e:
        print("Failed to load server-config.json, error: {}".format(e))


if __name__ == "__main__":
    import sys
    from xe_hack.xe_capture_output import resume_capture_all

    resume_capture_all()

    init_pid()

    _init_configs()

    _setup_data_and_symlinks()
    _setup_proxy()

    build_args(force_terminate_existing=True)
    prepare_environment()

    start()
