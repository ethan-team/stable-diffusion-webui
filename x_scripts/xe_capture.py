import sys
import os
import logging  

LOG_SYS_PRINT = "log/sys_print.txt"
LOG_DEFAULT = "log/sys_logging.log"

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


def _init_capture_handler():
    os.makedirs(os.path.dirname(LOG_DEFAULT), exist_ok=True)
    file_handler = logging.FileHandler(LOG_DEFAULT)

    # Configure the formatter for the file handler (optional)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s @ %(pathname)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


g_capture_log_handler = _init_capture_handler()


def hook_capture_handler():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

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

def capture_all():
    # Stop capturing the output
    g_capture.attach() 
    hook_capture_handler()


def recover_all():
    g_capture.dettach()


if __name__ == "__main__":
    print("firstline")
    capture_all()
    print("secondline")
    print("thirdline")
    recover_all()
    print("fourthline")

    logging.getLogger().info("info")


