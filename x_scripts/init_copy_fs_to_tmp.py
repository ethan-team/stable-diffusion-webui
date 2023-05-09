import os
import shutil


DIR_ROOT= os.path.dirname(os.path.dirname(__file__))


def get_fs_root():
    return "/root/autodl-fs/sdw"

def get_tmp_root():
    return "/root/autodl-tmp"


class DataDirSetup:
    @classmethod
    def _copy_data(cls, fldname):
        dir_src = f"{get_fs_root()}/{fldname}"
        dir_dst = f"{get_tmp_root()}/{fldname}"
        if not os.path.isdir(dir_src):
            raise ValueError(f"{dir_src} not exist")

        if not os.path.isdir(dir_dst):
            print(f"copy {dir_src} to {dir_dst}, it may take a while...")
            shutil.copytree(dir_src, dir_dst)
            print("copy done.")
        else:
            print(f"{dir_dst} exist, skip")
            
        return True, None

    @classmethod
    def ensure_data_copied(cls):
        cls._copy_data("models")
        #cls._copy_data("outputs")
        cls._copy_data("repositories")


if __name__ == "__main__":
    print(f"DIR_ROOT: {DIR_ROOT}")
    DataDirSetup.ensure_data_copied()