from logging.handlers import TimedRotatingFileHandler
import sys
import os
import threading
import logging
from datetime import datetime
from collections import namedtuple  
from logging import FileHandler

from torch import log_

# DIR_ROOT = os.path.dirname(os.path.dirname(__file__))
DIR_ROOT = "/root/autodl-tmp/plutus_log"

# LOG_ROUND_FILENAME = f"{DIR_ROOT}/plutus_log/hook_round.log"
# LOG_SYS_HOOK = f"{DIR_ROOT}/plutus_log/hook_thread.log"


THREAD_MEMO = namedtuple('THEAD_MEMO', 'obj_sys_stdout, obj_sys_stderr, obj_log_handler')
gmap_thread_memo = {}

gf_round_sys_stdout = False 
gf_round_log_handler = False 
log_writing_locked = False

current_work_idk = None
logger_webui: logging.Logger | None = None

def get_webui_logger() -> logging.Logger | None:
    global logger_webui
    global current_work_idk
    import x_hacked_launch

    # if x_hacked_launch.work_idk is None:
    #     return None

    if logger_webui is None:
        current_work_idk = x_hacked_launch.work_idk
        logger_webui = _create_webui_logger()
    elif x_hacked_launch.work_idk != current_work_idk:
        current_work_idk = x_hacked_launch.work_idk
        logger_webui = _create_webui_logger()

    return logger_webui


def _create_webui_logger() -> logging.Logger:
    global current_work_idk

    os.makedirs(os.path.join(DIR_ROOT, 'works'), exist_ok=True)

    if current_work_idk is None:
        ret = logging.getLogger("webui")
    else:
        ret = logging.getLogger(current_work_idk)
    ret.setLevel(logging.DEBUG)  # 你可以设置不同的日志级别

    if len(ret.handlers) == 0:
        if current_work_idk is not None:
            fh = FileHandler(os.path.join(DIR_ROOT, f'works/{current_work_idk}.log'))  # 输出到文件的 Handler
        else:
            fh = TimedRotatingFileHandler(os.path.join(DIR_ROOT, 'webui.log'), when='midnight', interval=1, backupCount=7)  # 输出到文件的 Handler

        fh.setLevel(logging.DEBUG)  # 输出到文件的日志级别
        fh_formatter = logging.Formatter('%(asctime)s [ThreadID: %(thread)d] [%(levelname)s]: %(message)s')
        fh.setFormatter(fh_formatter)

        ret.addHandler(fh)

    return ret


def _get_launch_mode():
    launch_mdoe = os.environ.get("LANUCH_MODE", "normal")
    return launch_mdoe


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
        global log_writing_locked

        if log_writing_locked:
            return
        
        log_writing_locked = True
        # Process the captured output as needed
        # For example, you can write it to a file, store it in a variable, etc.
        try:
            logger = get_webui_logger()
            if logger is not None:
                logger.info(text)
            # self.org_stdout.write(text)
        except: # noqa
            pass
        finally:
            log_writing_locked = False

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

def _hook_sys_stdout(obj_sys_stdout):
    global gf_round_sys_stdout
    # round_tag = None
    if obj_sys_stdout is not None and hasattr(obj_sys_stdout, "attach"):
        obj_sys_stdout.attach()
        # _, round_tag = _get_round_tag()

    if not gf_round_sys_stdout:
        # print(f"\n\n{round_tag}\n\n")
        gf_round_sys_stdout = True

def _unhook_sys_stdout(obj_sys_stdout):
    if obj_sys_stdout is not None and hasattr(obj_sys_stdout, "dettach"):
        obj_sys_stdout.dettach()

class _StderrCapture:
    def __init__(self):
        pass

    def attach(self):
        self.org_stderr = sys.stdout
        sys.stderr = self

    def dettach(self):
        if hasattr(self, 'org_stderr'):
            sys.stderr = self.org_stderr

    def write(self, text):
        global log_writing_locked

        if log_writing_locked:
            return
        
        log_writing_locked = True
        # Process the captured output as needed
        # For example, you can write it to a file, store it in a variable, etc.

        try:
            # get_webui_logger().error(text)
            logger = get_webui_logger()
            if logger is not None:
                logger.error(text)
            # with open(LOG_SYS_OUTPUT, 'a+') as f:
            #     f.write(text)
            # self.org_stderr.write(text)
        except: # noqa
            pass
        finally:
            log_writing_locked = False

    def flush(self):
        if hasattr(self, 'org_stderr'):
            self.org_stderr.flush()

    def isatty(self):
        return True

    def __getattr__(self, name):
        # Forward any other attribute access to the original sys.stdout
        if hasattr(self, 'org_stderr'):
            return getattr(self.org_stderr, name)
        return None

def _hook_sys_stderr(obj_sys_stderr):
    global gf_round_sys_stdout
    if obj_sys_stderr is not None and hasattr(obj_sys_stderr, "attach"):
        obj_sys_stderr.attach()

    if not gf_round_sys_stdout:
        gf_round_sys_stdout = True

def _unhook_sys_stderr(obj_sys_stderr):
    if obj_sys_stderr is not None and hasattr(obj_sys_stderr, "dettach"):
        obj_sys_stderr.dettach()


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


def _hook_logging_capture_handler(obj_logger_handler):
    global gf_round_log_handler
    root_logger = logging.getLogger()

    launch_mode = _get_launch_mode()
    if launch_mode.find("debug") != -1:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    if obj_logger_handler not in root_logger.handlers:
        # Attach the file handler to the root logger
        root_logger.addHandler(obj_logger_handler)

    # Get all existing loggers
    all_loggers = logging.Logger.manager.loggerDict.values()

    # Attach the file handler to all loggers
    for logger in all_loggers:
        if hasattr(logger, "addHandler") and hasattr(logger, "handlers"):
            # 判断logger是否Logger类型
            if not isinstance(logger, logging.Logger):
                continue

            if obj_logger_handler not in logger.handlers:
                logger.addHandler(obj_logger_handler)

    if not gf_round_log_handler:
        gf_round_log_handler = True


def _unhook_logging_capture_handler(obj_logger_handler):
    pass

# def _log_hook_thread():
#     try:
#         import os
#         import asyncio

#         thread_id = threading.get_ident()
#         pid = os.getpid()

#         loop_id = None
#         try:
#             loop_id = asyncio.get_running_loop().__hash__()
#         except: # noqa
#             pass

#         # msg = f'pid:{pid} thid:{thread_id} lpid:{loop_id}\n'
#         # with open(LOG_SYS_HOOK, 'a+') as f:
#         #     f.write(msg)
#     except: # noqa
#         pass

def _hook_thread():
    global gmap_thread_memo
    thread_id = threading.get_ident()
    if thread_id not in gmap_thread_memo:
        # _log_hook_thread()

        # Start capturing the output
        obj_sys_stdout = _StdoutCapture()
        _hook_sys_stdout(obj_sys_stdout)

        obj_sys_stderr = _StderrCapture()
        _hook_sys_stderr(obj_sys_stderr)

        # _hook_logging_capture_handler(obj_log_handler)

        # gmap_thread_memo[thread_id] = THREAD_MEMO(obj_sys_stdout=obj_sys_stdout, 
        #                                           obj_sys_stderr=obj_sys_stderr,
        #                                           obj_log_handler=obj_log_handler)
        print(f"_hook_thead {thread_id}")

    # return gmap_thread_memo[thread_id]

def _unhook_thread():
    pass

def resume_capture_all():
    _hook_thread()

def restore_capture_all():
    _unhook_thread()


if __name__ == "__main__":
    print("firstline")
    resume_capture_all()
    print("secondline")
    print("thirdline")
    restore_capture_all()
    print("fourthline")

    logging.getLogger().info("info")


