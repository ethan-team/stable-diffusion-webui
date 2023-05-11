import os

AUTODL_REGION = "AutoDLRegion"

def setup_proxy_env():
    val = os.environ.get(AUTODL_REGION, None)
    if val is None:
        return False
    
    if val.find("neimeng") != -1:
        proxy_addr = "http://192.168.1.174:12798"
    elif val.find("suqian") != -1:
        proxy_addr = "http://192.168.1.174:12798"
    else:
        proxy_addr = None
    
    if proxy_addr is None:
        return False
    
    os.environ["http_proxy"] = proxy_addr
    os.environ["https_proxy"] = proxy_addr
    print()
    print(f"autodl region:{val} proxy set to {proxy_addr}") 
    print()
    return True       


if __name__ == "__main__":
    setup_proxy_env()
