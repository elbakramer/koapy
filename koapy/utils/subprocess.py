import inspect
import subprocess
import sys
import textwrap

from koapy.config import config
from koapy.utils.platform import is_32bit, is_64bit


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


def get_executable_from_conda_envname(envname):
    return subprocess.check_output(
        [
            "conda",
            "run",
            "-n",
            envname,
            "python",
            "-c",
            "import sys; print(sys.executable)",
        ],
        encoding=sys.stdout.encoding,
        creationflags=subprocess.CREATE_NO_WINDOW,
    ).strip()


def get_executable_from_conda_envpath(envpath):
    return subprocess.check_output(
        [
            "conda",
            "run",
            "-p",
            envpath,
            "python",
            "-c",
            "import sys; print(sys.executable)",
        ],
        encoding=sys.stdout.encoding,
        creationflags=subprocess.CREATE_NO_WINDOW,
    ).strip()


def get_executable_from_executable_config(executable_config):
    if isinstance(executable_config, str):
        return executable_config
    if isinstance(executable_config, dict):
        if "path" in executable_config:
            return executable_config["path"]
        if "conda" in executable_config:
            conda_config = executable_config["conda"]
            if isinstance(conda_config, str):
                envname = conda_config
                return get_executable_from_conda_envname(envname)
            if isinstance(conda_config, dict):
                if "name" in conda_config:
                    envname = conda_config["name"]
                    return get_executable_from_conda_envname(envname)
                if "path" in conda_config:
                    envpath = conda_config["path"]
                    return get_executable_from_conda_envpath(envpath)


def get_32bit_executable():
    if is_32bit():
        return sys.executable
    executable_config = config.get("koapy.python.executable.32bit")
    return get_executable_from_executable_config(executable_config)


def get_64bit_executable():
    if is_64bit():
        return sys.executable
    executable_config = config.get("koapy.python.executable.64bit")
    return get_executable_from_executable_config(executable_config)


def run_file(filename, *args, executable=None, **kwargs):
    if executable is None:
        executable = sys.executable
    cmd = [executable, filename]
    return subprocess.run(cmd, *args, **kwargs)


def run_script(script, *args, executable=None, **kwargs):
    if executable is None:
        executable = sys.executable
    cmd = [executable, "-c", script]
    return subprocess.run(cmd, *args, **kwargs)


def run_function(function, *args, executable=None, **kwargs):
    script = function_to_script(function)
    return run_script(script, *args, executable=executable, **kwargs)
