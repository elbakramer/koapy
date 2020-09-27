import logging
import threading
import subprocess

from koapy.grpc.KiwoomOpenApiServiceClient import KiwoomOpenApiServiceClient

from koapy.config import config
from koapy.utils.networking import get_free_localhost_port
from koapy.utils.logging import verbosity_to_loglevel, set_loglevel

class KiwoomOpenApiContext:

    def __init__(self, port=None, client_check_timeout=None, verbosity=None, log_level=None):
        self._port = port or config.get('koapy.grpc.port') or get_free_localhost_port()
        self._client_check_timeout = client_check_timeout
        self._verbosity = verbosity
        if log_level is None:
            if self._verbosity is not None:
                log_level = verbosity_to_loglevel(self._verbosity)
        self._log_level = log_level
        if self._log_level is not None:
            set_loglevel(self._log_level)
        self._server_proc_args = [
            'python', '-m', 'koapy.pyqt5.tools.start_tray_application',
            '--port', str(self._port)]
        if self._verbosity:
            self._server_proc_args.append('-' + 'v' * self._verbosity)
        self._server_proc = None
        self._server_proc_terminate_timeout = config.get_int('koapy.grpc.context.server.terminate.timeout', 10)
        self._client = KiwoomOpenApiServiceClient(port=self._port)
        logging.debug('Testing if client is ready...')
        if not self._client.is_ready(client_check_timeout):
            logging.debug('Client is not ready, creating a new server')
            self._server_proc = subprocess.Popen(self._server_proc_args)
            assert self._client.is_ready()
            self._stub = self._client.get_stub()
        else:
            logging.debug('Client is ready, using existing server')
            self._stub = self._client.get_stub()
        self._lock = threading.RLock()
        self._enter_count = 0

    def __del__(self):
        self.close()

    def __enter__(self):
        with self._lock:
            self._enter_count += 1
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self._lock:
            self._enter_count -= 1
            if self._enter_count == 0:
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
