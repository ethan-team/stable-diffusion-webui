import os
from xe_run_core import build_args, prepare_environment, start

if __name__ == "__main__":
    os.environ["LANUCH_MODE"] = "normal"
    build_args()
    prepare_environment()
    start()
