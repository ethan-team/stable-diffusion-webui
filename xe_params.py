import os

class HackingParams:
    @staticmethod
    def need_extra_args():
        return True
    
    @staticmethod
    def need_update_git_repo():
        launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
        if launch_mdoe == "refresh":
            return True 
        return False
