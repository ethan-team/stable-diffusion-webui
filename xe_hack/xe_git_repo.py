import os
import sys
import subprocess
import errno
import logging
import socket
import re


logger = logging.getLogger()

g_git_info = None

def _run_command(commands, args, cwd=None, verbose=False, hide_stderr=False):
    assert isinstance(commands, list)
    p = None
    for c in commands:
        try:
            # remember shell=False, so use git.cmd on windows, not just git
            p = subprocess.Popen([c] + args,
                                 cwd=cwd,
                                 stdout=subprocess.PIPE,
                                 stderr=(subprocess.PIPE if hide_stderr else None))
            break
        except EnvironmentError as ex:
            logger.info("EnvironmentError: " + str(ex))
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                continue
            if verbose:
                logger.error("unable to run %s" % args[0])
                logger.error(e)
            return False, str(ex)
        except Exception as ex:
            logger.error("EnvironmentError: " + str(ex))
            return False, str(ex)

    else:
        if verbose:
            logger.error("unable to find command, tried %s" % (commands,))
        return False, ""
    stdout = p.communicate()[0].strip()
    if sys.version >= '3':
        stdout = stdout.decode()
    if p.returncode != 0:
        if verbose:
            logger.error("unable to run %s (error)" % args[0])
        return False, stdout
    return True, stdout


def _git_current_branch(root):
    if sys.platform == 'win32':
        lines = os.popen('git branch').readlines()
    else:
        lines = os.popen("git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \\(.*\\)/ (\\1)/'").readlines()
    line = lines[0].strip()
    line = line.replace("(", "")
    line = line.replace(")", "")
    return line

def _check_gv_type(git_ver_str):
    if git_ver_str is None:
        return "gv_empty"

    if "-dirty" in git_ver_str:
        return "gv_dirtry"
    if "-g" in git_ver_str:
        return "gv_not_tagged"
    return "gv_tagged"

def _git_versions_oneline(root, verbose=False):
    if not os.path.exists(os.path.join(root, ".git")):
        if verbose:
            logger.error("no .git in %s" % root)
            return
    lines = os.popen("git --no-pager log --decorate --pretty=oneline --abbrev-commit -1").readlines()
    line = lines[0].strip()
    return line


def git_versions_from_vcs(root=None, verbose=False):
    global g_git_info
    if g_git_info is not None:
        return g_git_info
    
    if root is None:
        root = os.path.dirname(os.path.dirname(__file__))

    # this runs 'git' from the root of the source tree. This only gets called
    # if the git-archive 'subst' keywords were *not* expanded, and
    # _version.py hasn't already been rewritten with a short version string,
    # meaning we're inside a checked out source tree.

    if not os.path.exists(os.path.join(root, ".git")):
        if verbose:
            logger.error("no .git in %s" % root)
        return {"version": None}

    GITS = ["git"]
    rc, stdout = _run_command(GITS,
                              ["describe", "--tags", "--dirty", "--always"],
                              cwd=root)
    if not rc:
        return {"version": None}
    tag = stdout
    rc, stdout = _run_command(GITS,
                              ["rev-parse", "HEAD"],
                              cwd=root)
    if stdout is None:
        return {"version": None} 

    full = stdout.strip()
    if tag.endswith("-dirty"):
        full += "-dirty"
    branch = _git_current_branch(root)

    gv_type = _check_gv_type(tag)

    oneline = _git_versions_oneline(root)

    hostname = socket.gethostname()

    ver_val = ver_value(tag)

    root_dir = root
    g_git_info = {"version": str(tag), "full": str(full), "ver_val": ver_val,
                  "branch": str(branch), 
                  "gv_type": str(gv_type), 'oneline':oneline, 
                  'hostname':hostname, "root_dir": root_dir}
    return g_git_info


def ver_value(version_or_tag):
    version = None
    value = 0
    if version_or_tag:
        if "_" in version_or_tag:
            pt = re.compile(r"^\S+_(\d+\.\d+\.\d+)$")
            versions = pt.findall(version_or_tag)
            if versions:
                version = versions[0]
        elif "-" in version_or_tag:
            version = version_or_tag.split("-")[0]
        else:
            version = version_or_tag
        pt = re.compile(r"^[m|v]\d+\.\d+\.\d+$")
        if pt.findall(version):
            version = version.replace("m","").replace("v","")
            ver_split = version.split(".")
            value = int(ver_split[0]) * 10000 + int(ver_split[1]) * 100 + int(ver_split[2])
    return value

def get_tag():
    git_info = git_versions_from_vcs()
    return git_info["version"]


if __name__ == "__main__":
    import pprint
    pprint.pprint(git_versions_from_vcs())

    print()
    print(get_tag())


