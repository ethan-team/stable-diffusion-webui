import os
import shutil


DIR_ROOT= os.path.dirname(os.path.dirname(__file__))

def is_symlink_directory(directory_path):
    return os.path.islink(directory_path) and os.path.isdir(directory_path)

class Symlinks:
    @classmethod
    def get_nas_root(cls):
        return "/root/autodl-fs"
    
    @classmethod
    def get_tmp_root(cls):
        return "/root/autodl-tmp"


class WorkingDirsSetup:
    @classmethod
    def _make_symlink(cls, fldname):
        dir_symlink_sys = f"{DIR_ROOT}/{fldname}"
        if is_symlink_directory(dir_symlink_sys):
            print(f"{dir_symlink_sys} is symbolic directory already")
            return True, None
        
        dir_fldname_linked_dst = f"{Symlinks.get_tmp_root()}/{fldname}"
        if not os.path.isdir(dir_fldname_linked_dst):
            os.makedirs(dir_fldname_linked_dst, exist_ok=True)
            print(f"{dir_fldname_linked_dst} is empty dir, and ready to use")
        
        if os.path.isdir(dir_symlink_sys):
            user_input = input(f"{dir_symlink_sys} is an existing dir, are you sure to make symbolic link to {dir_fldname_linked_dst} to save space? (y/n)")
            user_input = user_input.lower()
            if not user_input.startswith('y'):
                raise ValueError("setup failed")

        shutil.rmtree(dir_symlink_sys)
        os.symlink(dir_fldname_linked_dst, dir_symlink_sys, target_is_directory=True)
        return True, None

    @classmethod
    def ensure_working_dir(cls):
        cls._make_symlink("models")
        cls._make_symlink("outputs")
        cls._make_symlink("repositories")


if __name__ == "__main__":
    print(f"DIR_ROOT: {DIR_ROOT}")
    WorkingDirsSetup.ensure_working_dir()