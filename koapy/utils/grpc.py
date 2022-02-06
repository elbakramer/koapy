import contextlib
import threading
import warnings

from pprint import PrettyPrinter

import grpc

from google.protobuf.json_format import MessageToDict


@contextlib.contextmanager
def warn_on_rpc_error_context():
    try:
        yield
    except grpc.RpcError as e:
        warnings.warn(str(e))


def warn_on_rpc_error(stream):
    with warn_on_rpc_error_context():
        for event in stream:
            yield event


def cancel_after(stream, after):
    timer = threading.Timer(after, stream.cancel)
    timer.start()
    return warn_on_rpc_error(stream)


def pprint_message(message):
    pp = PrettyPrinter()
    pp.pprint(MessageToDict(message, preserving_proto_field_name=True))
