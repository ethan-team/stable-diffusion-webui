import os
from xe_run_core import build_args, prepare_environment, start
from x_scripts.init_autodl_proxy import setup_proxy_env
from x_scripts.init_copy_fs_to_tmp import DataDirSetup
from x_scripts.init_setup_symlink_dirs import SymlinkDirsSetup

if __name__ == "__main__":
    DataDirSetup.ensure_data_copied()
    SymlinkDirsSetup.ensure_working_dir()

    os.environ["LANUCH_MODE"] = "refresh"
    setup_proxy_env()
    build_args()
    prepare_environment()
    start()
