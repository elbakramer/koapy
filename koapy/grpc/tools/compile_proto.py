import os
import subprocess

from mslex import quote

def compile_proto():
    proto_filename = 'KiwoomOpenApiService.proto'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.realpath(os.path.join(file_dir, '..', '..', '..'))
    proto_path = project_dir
    proto_filepath = os.path.join(proto_path, 'koapy', 'grpc', proto_filename)
    python_out = proto_path
    grpc_python_out = proto_path
    cmd = ['python',
        '-m', 'grpc_tools.protoc',
        '--proto_path=%s' % quote(proto_path),
        '--python_out=%s' % quote(python_out),
        '--grpc_python_out=%s' % quote(grpc_python_out),
        proto_filepath,
    ]
    print(' '.join(cmd))
    subprocess.run(cmd, cwd=project_dir, check=True)

if __name__ == '__main__':
    compile_proto()
    