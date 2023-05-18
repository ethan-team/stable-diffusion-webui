import shutil
import os

class SnapshotCopier:
    def __init__(self):
        pass

    def _copy_model_from_src_to_dst(self, src_dir, dst_dir, symbolic=True):
        if not symbolic:
            ret = shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        else:
            os.makedirs(dst_dir, exist_ok=True)
            names = os.listdir(src_dir)
            for name in names:
                src_path = f"{src_dir}/{name}"
                dst_path = f"{dst_dir}/{name}"
                if os.path.isdir(src_path):
                    if os.path.isdir(dst_path):
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                else:
                    shutil.copy(src_path, dst_path)
            ret = True
        return ret

    def _get_sdw_model_dir(self):
        return "/root/stable-diffusion-webui/models/grounding-dino"

    def _get_snapshot_root(self):
        return '/root/.cache/huggingface/hub/models--ShilongLiu--GroundingDINO/snapshots'       

    def do_copy_snapshot_to_models(self, clean=False):
        cached_root = self._get_snapshot_root()

        cached_folder = None
        names = os.listdir(cached_root)
        for name in names:
            dname = f"{cached_root}/{name}"
            if os.path.isdir(dname):
                cached_folder = dname
                break

        print(f"cached_root: {cached_root}")
        print(f"cached_snapshot: {cached_folder}")
        if os.path.isdir(cached_folder):
            dst_dir = self._get_sdw_model_dir()
            try:
                if clean:
                    if os.path.isdir(dst_dir):
                        shutil.rmtree(dst_dir)
                os.makedirs(dst_dir, exist_ok=True)

                ret = self._copy_model_from_src_to_dst(cached_folder, dst_dir)
                print(f"new clean {dst_dir} has made: {ret}")
                return True
            except Exception as ex:
                print(ex)
                return False
        else:
            print(f"no valid cached_folder {cached_folder} found")
            return False
        

if __name__ == "__main__":
    shrcar = SnapshotCopier()
    shrcar.do_copy_snapshot_to_models()