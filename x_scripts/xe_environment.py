import sys
import os 

LOG_SYS_PRINT = "log/sys_print.txt"

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


def capture_sys_print():
    # Stop capturing the output
    g_capture.attach() 

def recover_sys_print():
    g_capture.dettach()


if __name__ == "__main__":
    print("firstline")
    capture_sys_print()
    print("secondline")
    print("thirdline")
    recover_sys_print()
    print("fourthline")


