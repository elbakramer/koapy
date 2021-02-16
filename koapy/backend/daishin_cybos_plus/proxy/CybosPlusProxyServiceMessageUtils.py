import os
import subprocess

def AssignPrimitive(message, value):
    if value is None:
        pass
    elif isinstance(value, str):
        message.string_value = value
    elif isinstance(value, int):
        message.long_value = value
    elif isinstance(value, bool):
        message.bool_value = value
    elif isinstance(value, float):
        message.float_value = value
    elif isinstance(value, list):
        for item in value:
            AssignPrimitive(message.list_value.values.add(), item)
    elif isinstance(value, tuple):
        for item in value:
            AssignPrimitive(message.tuple_value.values.add(), item)
    else:
        raise TypeError
    return message

def ExtractPrimitive(message):
    if message.HasField('string_value'):
        return message.string_value
    elif message.HasField('long_value'):
        return message.long_value
    elif message.HasField('bool_value'):
        return message.bool_value
    elif message.HasField('float_value'):
        return message.float_value
    elif message.HasField('list_value'):
        return list(ExtractPrimitive(value) for value in message.list_value.values)
    elif message.HasField('tuple_value'):
        return tuple(ExtractPrimitive(value) for value in message.tuple_value.values)

def Protoc():
    proto_filename = 'CybosPlusProxyService.proto'
    proto_filedir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.realpath(os.path.join(proto_filedir, '..', '..', '..'))
    proto_path = project_dir
    python_out = project_dir
    grpc_python_out = python_out
    proto_filepath = os.path.join(proto_filedir, proto_filename)
    cmd = [
        'python', '-m', 'grpc_tools.protoc',
        '--proto_path=%s' % proto_path,
        '--python_out=%s' % python_out,
        '--grpc_python_out=%s' % grpc_python_out,
        proto_filepath,
    ]
    _ = subprocess.run(cmd, cwd=project_dir, check=True)

if __name__ == '__main__':
    Protoc()
