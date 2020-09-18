import logging
import subprocess

from koapy.grpc.KiwoomOpenApiServiceClient import KiwoomOpenApiServiceClient

from koapy.config import config
from koapy.utils.networking import get_free_localhost_port

class KiwoomOpenApiContext:

    def __init__(self, port=None):
        self._port = port or config.get('koapy.grpc.port') or get_free_localhost_port()
        self._server_proc_args = [
            'python', '-m', 'koapy.pyqt5.tools.start_tray_application', '--port', str(self._port)]
        self._server_proc = None
        self._server_proc_terminate_timeout = config.get_int('koapy.grpc.context.server.terminate.timeout', 10)
        self._client = KiwoomOpenApiServiceClient(port=self._port)
        logging.debug('Testing if client is ready...')
        if not self._client.is_ready():
            logging.debug('Client is not ready, creating a new server')
            self._server_proc = subprocess.Popen(self._server_proc_args)
            assert self._client.is_ready()
        else:
            logging.debug('Client is ready, using existing server')
        self._stub = self._client.get_stub()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_stub(self):
        return self._stub

    def close(self):
        self._client.close()
        if self._server_proc is not None:
            self._server_proc.terminate() # maybe soft termination available via grpc? rather than hard termination
            self._server_proc.wait(self._server_proc_terminate_timeout)
            self._server_proc = None

    def __getattr__(self, name):
        return getattr(self._stub, name)
