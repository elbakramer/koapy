import subprocess

from pathlib import Path


def compile_proto():
    proto_filename = "KiwoomOpenApiPlusService.proto"
    file_path = Path(__file__)
    file_dir = file_path.parent
    project_dir = file_dir.parent.parent.parent.parent.parent
    proto_path = project_dir
    proto_filepath = (
        proto_path
        / "koapy"
        / "backend"
        / "kiwoom_open_api_plus"
        / "grpc"
        / proto_filename
    )
    python_out = project_dir
    grpc_python_out = python_out
    cmd = [
        "python",
        "-m",
        "grpc_tools.protoc",
        "--proto_path=%s" % str(proto_path),
        "--python_out=%s" % str(python_out),
        "--grpc_python_out=%s" % str(grpc_python_out),
        str(proto_filepath),
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd, cwd=project_dir)


if __name__ == "__main__":
    compile_proto()
