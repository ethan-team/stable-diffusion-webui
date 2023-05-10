import os

def _get_launch_mode():
    launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
    return launch_mdoe

class HackingParams:
    @staticmethod
    def need_extra_args():
        return True
    
    @staticmethod
    def need_update_git_repo():
        launch_mdoe = _get_launch_mode()
        if launch_mdoe.find("refresh") != -1:
            return True 
        return False
    
    @staticmethod
    def need_update_extensions():
        launch_mdoe = _get_launch_mode()        
        if launch_mdoe.find("refresh") != -1:
            return True 
        return False

    @staticmethod
    def need_debug():
        launch_mdoe = _get_launch_mode()        
        if launch_mdoe.find("debug") != -1:
            return True 
        return False     
