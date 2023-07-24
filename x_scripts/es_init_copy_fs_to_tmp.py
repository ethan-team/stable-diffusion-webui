import os
import shutil


DIR_ROOT= os.path.dirname(os.path.dirname(__file__))


def get_fs_root():
    return "/root/autodl-fs/albert/models"

def get_tmp_root():
    return "/root/autodl-tmp"


def copytree_with_progress(src, dst):
    total_files = sum(len(files) for _, _, files in os.walk(src))
    files_copied = 0

    def copy_progress(src, dst):
        nonlocal files_copied
        file_size = os.path.getsize(src)
        print(f"Copying file ({files_copied}/{total_files})/len:{file_size:,}: {src} -> {dst} ")
        shutil.copy2(src, dst)
        files_copied += 1

    shutil.copytree(src, dst, copy_function=copy_progress)


class DataDirSetup:
    @classmethod
    def _copy_data(cls, fldname):
        dir_src = f"{get_fs_root()}/{fldname}"
        dir_dst = f"{get_tmp_root()}/{fldname}"
        if not os.path.isdir(dir_src):
            raise ValueError(f"{dir_src} not exist")

        if not os.path.isdir(dir_dst):
            print()
            print(f"Copying {dir_src} to {dir_dst}, it may take a while...")
            copytree_with_progress(dir_src, dir_dst)
            print("Copy done.")
            print()
        else:
            print(f"{dir_dst} exist, skip")
            
        return True, None

    @classmethod
    def ensure_data_copied(cls):
        cls._copy_data("models")
        #cls._copy_data("outputs")
        #cls._copy_data("repositories")


if __name__ == "__main__":
    print(f"DIR_ROOT: {DIR_ROOT}")
    DataDirSetup.ensure_data_copied()