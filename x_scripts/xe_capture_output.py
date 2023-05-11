import sys
import os
import logging
from datetime import datetime  


LOG_SYS_PRINT = "log/sys_print.txt"
LOG_DEFAULT = "log/sys_logging.log"
ROUND_FILENAME = "log/round.log"

g_capture_sys_print = False 
g_capture_sys_logging = False
g_round_num = None 

def _get_launch_mode():
    launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
    return launch_mdoe


def _get_round_tag():
    global g_round_num
    os.makedirs(os.path.dirname(ROUND_FILENAME), exist_ok=True)
    if g_round_num is None:
        if not os.path.isfile(ROUND_FILENAME):
            round = 1
        else:
            with open(ROUND_FILENAME, 'r') as f:
                lines = f.readlines()
                line = lines[-1]
                round = int(line)

            round += 1
        with open(ROUND_FILENAME, 'w+') as f:
            f.write(f"{round}\n")
        g_round_num = round
    round_tag = f"\'round {g_round_num}\' @ {datetime.now()}"
    return g_round_num, round_tag


class OutputCapture:
    def __init__(self):
        os.makedirs(os.path.dirname(LOG_SYS_PRINT), exist_ok=True)

    def attach(self):
        self.org_stdout = sys.stdout
        sys.stdout = self

    def dettach(self):
        sys.stdout = self.org_stdout

    def write(self, text):
        # Process the captured output as needed
        # For example, you can write it to a file, store it in a variable, etc.
        with open(LOG_SYS_PRINT, 'a+') as f:
            f.write(text)
        self.org_stdout.write(text)

    def flush(self):
        self.org_stdout.flush()

    def isatty(self):
        return True
    
    def __getattr__(self, name):
        # Forward any other attribute access to the original sys.stdout
        return getattr(self.org_stdout, name)


# Start capturing the output
g_capture = OutputCapture()


def _init_logging_capture_handler():
    os.makedirs(os.path.dirname(LOG_DEFAULT), exist_ok=True)
    file_handler = logging.FileHandler(LOG_DEFAULT)

    # Configure the formatter for the file handler (optional)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s @ %(pathname)s')
    file_handler.setFormatter(formatter)

    launch_mode = _get_launch_mode()
    if launch_mode.find("debug") != -1:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)        
    return file_handler


g_capture_log_handler = _init_logging_capture_handler()


def hook_logging_capture_handler():
    global g_capture_sys_logging
    root_logger = logging.getLogger()

    launch_mode = _get_launch_mode()
    if launch_mode.find("debug") != -1:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    if g_capture_log_handler not in root_logger.handlers:
        # Attach the file handler to the root logger
        root_logger.addHandler(g_capture_log_handler)

    # Get all existing loggers
    all_loggers = logging.Logger.manager.loggerDict.values()

    # Attach the file handler to all loggers
    for logger in all_loggers:
        if hasattr(logger, "addHandler") and hasattr(logger, "handlers"):
            if g_capture_log_handler not in logger.handlers:
                logger.addHandler(g_capture_log_handler)

    if not g_capture_sys_logging:
        _, round_tag = _get_round_tag()
        root_logger.info("  ")
        root_logger.info("  ")
        root_logger.info(f"{round_tag}")
        root_logger.info("  ")
        root_logger.info("  ")
        g_capture_sys_logging = True

def unhook_logging_capture_handler():
    pass

def hook_sys_output():
    global g_capture_sys_print
    g_capture.attach()
    if not g_capture_sys_print:
        _, round_tag = _get_round_tag()
        print(f"\n\n{round_tag}\n\n")
        g_capture_sys_print = True     

def unhook_sys_output():
    g_capture.dettach()    

def capture_all():
    hook_sys_output()
    hook_logging_capture_handler()

def recover_all():
    unhook_sys_output()
    unhook_logging_capture_handler()


if __name__ == "__main__":
    print("firstline")
    capture_all()
    print("secondline")
    print("thirdline")
    recover_all()
    print("fourthline")

    logging.getLogger().info("info")


