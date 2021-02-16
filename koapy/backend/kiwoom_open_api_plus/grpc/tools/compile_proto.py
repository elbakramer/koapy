import os
import subprocess

def compile_proto():
    proto_filename = 'KiwoomOpenApiPlusService.proto'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.realpath(os.path.join(file_dir, '..', '..', '..', '..', '..'))
    proto_path = project_dir
    proto_filepath = os.path.join(proto_path, 'koapy', 'backend', 'kiwoom_open_api_plus', 'grpc', proto_filename)
    python_out = project_dir
    grpc_python_out = python_out
    cmd = [
        'python', '-m', 'grpc_tools.protoc',
        '--proto_path=%s' % proto_path,
        '--python_out=%s' % python_out,
        '--grpc_python_out=%s' % grpc_python_out,
        proto_filepath]
    print(' '.join(cmd))
    subprocess.run(cmd, cwd=project_dir, check=True)

if __name__ == '__main__':
    compile_proto()
