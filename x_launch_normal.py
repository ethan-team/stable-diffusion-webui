import os
from xe_launch_core import build_args, prepare_environment, start

if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal"
    build_args()
    prepare_environment()
    start()
