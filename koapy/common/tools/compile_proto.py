import subprocess
import sys

from pathlib import Path


def main():
    script_dir = Path(__file__).parent.resolve()
    proto_filedir = script_dir.parent.resolve()
    proto_filename = "DispatchProxyService.proto"
    project_dir = proto_filedir.parent.parent.resolve()
    proto_path = project_dir
    python_out = project_dir
    grpc_python_out = python_out
    proto_filepath = proto_filedir / proto_filename
    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto_path}",
        f"--python_out={python_out}",
        f"--grpc_python_out={grpc_python_out}",
        f"{proto_filepath}",
    ]
    return subprocess.check_call(cmd, cwd=project_dir)


if __name__ == "__main__":
    main()
