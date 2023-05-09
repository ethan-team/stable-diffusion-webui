import os

def _need_extra_args():
    return True

def _need_update_git_repo():
    launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
    if launch_mdoe == "refresh":
        return True 
    return False

class HackingParams:
    ADD_ARGS = _need_extra_args()
    UPDATE_GIT_REPO = _need_update_git_repo()
