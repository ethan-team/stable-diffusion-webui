import os
import socket

def _get_launch_mode():
    launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
    return launch_mdoe

class HackingParams:
    @staticmethod
    def need_extra_common_args():
        return True
    
    @staticmethod
    def need_update_repositories():
        #Do not auto update repositories, using manual only
        #launch_mdoe = _get_launch_mode()
        #if launch_mdoe.find("update_repo") != -1:
        #    return True 
        return False

    @staticmethod
    def need_debug():
        launch_mdoe = _get_launch_mode()        
        if launch_mdoe.find("debug") != -1:
            return True 
        return False 

    @staticmethod
    def need_add_extensions():
        launch_mdoe = _get_launch_mode()        
        if launch_mdoe.find("refresh") != -1:
            return True 
        return False            

    @staticmethod
    def prepare_env_vars():
        try:
            hostname = socket.gethostname()
            hostname = hostname.replace("autodl-container-", "")
            hostname = hostname.replace("container-", "")

            from xe_hack.xe_git_repo import get_tag
            tag = get_tag()

            hostid = f"{tag} @{hostname}"
            os.environ["HOSTID"] = hostid

        except:
            pass

