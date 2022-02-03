import inspect
import subprocess
import sys
import textwrap

from koapy.utils.logging import get_logger

logger = get_logger(__name__)


def function_to_script(func):
    function_sig = inspect.signature(func)
    assert all(
        p.default != p.empty for p in function_sig.parameters
    ), "Function should not require any parameters"

    function_name = func.__name__
    function_impl = inspect.getsource(func)
    function_impl = textwrap.dedent(function_impl)

    script = (
        textwrap.dedent(
            """
    %s

    if __name__ == '__main__':
        %s()
    """
        )
        % (function_impl, function_name)
    )

    return script


def function_to_subprocess_args(func, executable=None):
    if executable is None:
        executable = sys.executable
    script = function_to_script(func)
    args = [executable, "-c", script]
    return args


def run_file(filename, *args, executable=None, **kwargs):
    if executable is None:
        executable = sys.executable
    cmd = [executable, filename]
    return subprocess.check_call(cmd, *args, **kwargs)


def run_script(script, *args, executable=None, **kwargs):
    if executable is None:
        executable = sys.executable
    cmd = [executable, "-c", script]
    return subprocess.check_call(cmd, *args, **kwargs)


def run_function(function, *args, executable=None, **kwargs):
    script = function_to_script(function)
    return run_script(script, *args, executable=executable, **kwargs)


def quote(s):
    return '"' + s.replace('"', '`"') + '"'


def run_as_admin(cmd, cwd=None, check=True, wait=True):
    import win32con
    import win32event
    import win32process

    # pyright: reportMissingImports=false
    # pylint: disable=import-error,no-name-in-module
    from win32com.shell import shellcon
    from win32com.shell.shell import ShellExecuteEx

    kwargs = dict(
        nShow=win32con.SW_SHOWNORMAL,
        fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
        lpVerb="runas",
        lpFile=cmd[0],
        lpParameters=" ".join(cmd[1:]),
    )

    if cwd is not None:
        kwargs["lpDirectory"] = cwd

    logger.info("Running command: %s", " ".join(cmd))
    procInfo = ShellExecuteEx(**kwargs)

    if check or wait:
        procHandle = procInfo["hProcess"]
        _ = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        logger.info("Process handle %s returned code %d", procHandle, rc)
        if check and rc < 0:
            raise subprocess.CalledProcessError(rc, cmd)
    else:
        rc = None

    return rc


def create_job_object_for_cleanup():
    # https://stackoverflow.com/questions/23434842/python-how-to-kill-child-processes-when-parent-dies/23587108#23587108s
    import win32job

    jobAttributes = None
    jobName = ""
    hJob = win32job.CreateJobObject(jobAttributes, jobName)
    extendedInfo = win32job.QueryInformationJobObject(
        hJob, win32job.JobObjectExtendedLimitInformation
    )
    basicLimitInformation = extendedInfo["BasicLimitInformation"]
    basicLimitInformation["LimitFlags"] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    win32job.SetInformationJobObject(
        hJob,
        win32job.JobObjectExtendedLimitInformation,
        extendedInfo,
    )
    return hJob


job_handle = create_job_object_for_cleanup()


def make_process_die_when_parent_dies(pid):
    assert pid != 0

    # https://stackoverflow.com/questions/23434842/python-how-to-kill-child-processes-when-parent-dies/23587108#23587108s
    import win32api
    import win32con
    import win32job

    desiredAccess = win32con.PROCESS_TERMINATE | win32con.PROCESS_SET_QUOTA
    inheritHandle = False
    hProcess = win32api.OpenProcess(
        desiredAccess,
        inheritHandle,
        pid,
    )
    # process will be terminated when job is destroyed
    # job will be destroyed when its last handle is closed
    # job handle will be closed when it loses its reference, hJob in this case
    hJob = job_handle
    win32job.AssignProcessToJobObject(hJob, hProcess)


class Popen(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        make_process_die_when_parent_dies(self.pid)
