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
        dir_fldname = f"{DIR_ROOT}/{fldname}"
        if is_symlink_directory(dir_fldname):
            print(f"{dir_fldname} is symbolic directory")
            return True, None
        
        dir_fldname_linked = f"{Symlinks.get_tmp_root()}/{fldname}"
        #if os.path.isdir(dir_fldname_linked):
        #    print(f"{dir_fldname_linked} existed already")
        #    return False, None
        
        os.makedirs(dir_fldname_linked, exist_ok=True)
        os.symlink(dir_fldname_linked, dir_fldname, target_is_directory=True)
        return True, None


    @classmethod
    def ensure_working_dir(cls):
        cls._make_symlink("models")
        cls._make_symlink("outputs")



if __name__ == "__main__":
    print(f"DIR_ROOT: {DIR_ROOT}")
    WorkingDirsSetup.ensure_working_dir()