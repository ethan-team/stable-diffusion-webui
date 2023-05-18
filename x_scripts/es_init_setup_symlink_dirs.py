import os
import shutil


DIR_ROOT= os.path.dirname(os.path.dirname(__file__))

def is_symlink_directory(directory_path):
    return os.path.isdir(directory_path) and os.path.islink(directory_path) 


def get_tmp_root():
    return "/root/autodl-tmp"


class SymlinkDirsSetup:
    @classmethod
    def _make_symlink(cls, fldname, backup=False):
        dir_symlink_sys = f"{DIR_ROOT}/{fldname}"
        if is_symlink_directory(dir_symlink_sys):
            print(f"{dir_symlink_sys} is symbolic directory already")
            return True, None
        
        dir_fldname_linked_dst = f"{get_tmp_root()}/{fldname}"
        if not os.path.isdir(dir_fldname_linked_dst):
            os.makedirs(dir_fldname_linked_dst, exist_ok=True)
            print(f"{dir_fldname_linked_dst} is empty dir, and ready to use")
        
        if os.path.isdir(dir_symlink_sys):
            if not is_symlink_directory(dir_symlink_sys):
                if backup:
                    dir_symlink_sys_bak = dir_symlink_sys + "_bak"
                    print(f"Backup {dir_symlink_sys} to {dir_symlink_sys_bak} ")
                    shutil.move(dir_symlink_sys, dir_symlink_sys_bak)
                shutil.rmtree(dir_symlink_sys)
        
        if not is_symlink_directory(dir_symlink_sys):
            print(f"Create symlink from {dir_symlink_sys} to {dir_fldname_linked_dst}")
            os.symlink(dir_fldname_linked_dst, dir_symlink_sys, target_is_directory=True)
        return True, None

    @classmethod
    def ensure_working_dir(cls):
        cls._make_symlink("models")
        cls._make_symlink("outputs", backup=True)
        #cls._make_symlink("repositories")


if __name__ == "__main__":
    print(f"DIR_ROOT: {DIR_ROOT}")
    SymlinkDirsSetup.ensure_working_dir()