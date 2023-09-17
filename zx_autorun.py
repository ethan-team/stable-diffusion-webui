#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time

import portalocker

DIR_ROOT = os.path.dirname(__file__)

LOCK_FILE = os.path.join(DIR_ROOT, 'webui.lock')

def is_single_instance():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, 'r') as f:
            try:
                portalocker.lock(f, portalocker.LOCK_EX | portalocker.LOCK_NB)
                return True
            except portalocker.LockException:
                return False
    else:
        return True

def main_program():
    while True:
        # 主程序
        try:
            subprocess.check_call(['python', 'zz_normal_launch.py'])
        except subprocess.CalledProcessError as e:
            print(e)
            pass

        print("Webui is running...")
        time.sleep(1)


if __name__ == "__main__":
    # print(f"{__file__} kicked @{DIR_ROOT}")
    if is_single_instance():
        with open(LOCK_FILE, 'w') as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            try:
                main_program()
            finally:
                os.remove(LOCK_FILE)
    else:
        print("Error: Program is running...")
        sys.exit(1)


