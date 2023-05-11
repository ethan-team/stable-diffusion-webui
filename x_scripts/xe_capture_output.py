import sys
import os
import logging
from datetime import datetime  


LOG_SYS_PRINT = "log/sys_print.txt"
LOG_DEFAULT = "log/sys_logging.log"
ROUND_FILENAME = "log/round.log"

gf_capture_sys_print = False 
gf_capture_sys_logging = False
gf_round_num = None 

try:
    os.makedirs(os.path.dirname(LOG_DEFAULT), exist_ok=True)
except:  # noqa
    pass

def _get_launch_mode():
    launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
    return launch_mdoe

def _get_round_tag():
    global gf_round_num
    if gf_round_num is None:
        round = 1
        try:
            if os.path.isfile(ROUND_FILENAME):
                with open(ROUND_FILENAME, 'r') as f:
                    lines = f.readlines()
                    line = lines[-1]
                    round = int(line)

                round += 1
            with open(ROUND_FILENAME, 'w+') as f:
                f.write(f"{round}\n")
        except: # noqa
            pass
        gf_round_num = round
    round_tag = f"\'round {gf_round_num}\' @ {datetime.now()}"
    return gf_round_num, round_tag


class _StdoutCapture:
    def __init__(self):
        pass

    def attach(self):
        self.org_stdout = sys.stdout
        sys.stdout = self

    def dettach(self):
        if hasattr(self, 'org_stdout'):
            sys.stdout = self.org_stdout

    def write(self, text):
        # Process the captured output as needed
        # For example, you can write it to a file, store it in a variable, etc.
        try:
            with open(LOG_SYS_PRINT, 'a+') as f:
                f.write(text)
            self.org_stdout.write(text)
        except: # noqa
            pass

    def flush(self):
        if hasattr(self, 'org_stdout'):
            self.org_stdout.flush()

    def isatty(self):
        return True
    
    def __getattr__(self, name):
        # Forward any other attribute access to the original sys.stdout
        if hasattr(self, 'org_stdout'):
            return getattr(self.org_stdout, name)
        return None


# Start capturing the output
g_capture_sys_stdout = _StdoutCapture()

def _hook_sys_stdout():
    global gf_capture_sys_print
    if not gf_capture_sys_print:
        g_capture_sys_stdout.attach()
        _, round_tag = _get_round_tag()
        print(f"\n\n{round_tag}\n\n")
        gf_capture_sys_print = True     

def _unhook_sys_stdout():
    global gf_capture_sys_print
    if gf_capture_sys_print:
        g_capture_sys_stdout.dettach()
        gf_capture_sys_print = False  


class _PlainLoggerHandler(logging.FileHandler):
    def __init__(self, pathname):
        super(_PlainLoggerHandler, self).__init__(pathname)

        launch_mode = _get_launch_mode()
        if launch_mode.find("debug") != -1:
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logging.INFO)  
        self.setFormatter(logging.Formatter('%(asctime)s@%(process)d - %(levelname)s - %(message)s @ %(pathname)s'))

    def emit(self, record):
        try:
            super(_PlainLoggerHandler, self).emit(record)
        except: # noqa
            pass


g_capture_plain_logger_handler = _PlainLoggerHandler(LOG_DEFAULT)


def _hook_logging_capture_handler():
    global gf_capture_sys_logging
    root_logger = logging.getLogger()

    if g_capture_plain_logger_handler is not None: 

        launch_mode = _get_launch_mode()
        if launch_mode.find("debug") != -1:
            root_logger.setLevel(logging.DEBUG)
        else:
            root_logger.setLevel(logging.INFO)

        if g_capture_plain_logger_handler not in root_logger.handlers:
            # Attach the file handler to the root logger
            root_logger.addHandler(g_capture_plain_logger_handler)

        # Get all existing loggers
        all_loggers = logging.Logger.manager.loggerDict.values()

        # Attach the file handler to all loggers
        for logger in all_loggers:
            if hasattr(logger, "addHandler") and hasattr(logger, "handlers"):
                if g_capture_plain_logger_handler not in logger.handlers:
                    logger.addHandler(g_capture_plain_logger_handler)

        if not gf_capture_sys_logging:
            _, round_tag = _get_round_tag()
            root_logger.info("  ")
            root_logger.info("  ")
            root_logger.info(f"{round_tag}")
            root_logger.info("  ")
            root_logger.info("  ")
            gf_capture_sys_logging = True

def _unhook_logging_capture_handler():
    pass
  

def capture_all():
    _hook_sys_stdout()
    _hook_logging_capture_handler()

def recover_all():
    _unhook_sys_stdout()
    _unhook_logging_capture_handler()


if __name__ == "__main__":
    print("firstline")
    capture_all()
    print("secondline")
    print("thirdline")
    recover_all()
    print("fourthline")

    logging.getLogger().info("info")


