import sys
import threading
import subprocess

from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import KiwoomOpenApiPlusServiceClient
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypointMixin import KiwoomOpenApiPlusEntrypointMixin

from koapy.config import config
from koapy.utils.networking import get_free_localhost_port
from koapy.utils.logging import verbosity_to_loglevel, loglevel_to_verbosity, set_loglevel
from koapy.utils.logging.Logging import Logging

class KiwoomOpenApiPlusEntrypoint(KiwoomOpenApiPlusEntrypointMixin, Logging):

    def __init__(self, port=None, client_check_timeout=None, verbosity=None, log_level=None):
        if port is None:
            port = config.get('koapy.backend.kiwoom_open_api_plus.grpc.port', 0) or get_free_localhost_port()

        if log_level is None and verbosity is not None:
            log_level = verbosity_to_loglevel(verbosity)
        if verbosity is None and log_level is not None:
            verbosity = loglevel_to_verbosity(log_level)

        self._port = port
        self._client_check_timeout = client_check_timeout
        self._verbosity = verbosity
        self._log_level = log_level

        if self._log_level is not None:
            set_loglevel(self._log_level)

        self._server_executable = config.get('koapy.context.server.executable', None)
        if not isinstance(self._server_executable, str):
            self._server_executable = None
        if self._server_executable is None:
            envpath = config.get('koapy.context.server.executable.conda.envpath', None)
            if envpath is not None and isinstance(envpath, str):
                self._server_executable = subprocess.check_output([ # pylint: disable=unexpected-keyword-arg
                    'conda', 'run', '-p', envpath,
                    'python', '-c', 'import sys; print(sys.executable)',
                ], encoding=sys.stdout.encoding, creationflags=subprocess.CREATE_NO_WINDOW).strip()
        if self._server_executable is None:
            envname = config.get('koapy.context.server.executable.conda.envname', None)
            if envname is not None and isinstance(envname, str):
                self._server_executable = subprocess.check_output([ # pylint: disable=unexpected-keyword-arg
                    'conda', 'run', '-n', envname,
                    'python', '-c', 'import sys; print(sys.executable)',
                ], encoding=sys.stdout.encoding, creationflags=subprocess.CREATE_NO_WINDOW).strip()
        if self._server_executable is None:
            self._server_executable = sys.executable

        self._server_proc_args = [self._server_executable, '-m', 'koapy.cli', 'serve']
        if self._port is not None:
            self._server_proc_args.extend(['-p', str(self._port)])
        if self._verbosity is not None:
            self._server_proc_args.extend(['-' + 'v' * self._verbosity])

        self._server_proc = None
        self._server_proc_terminate_timeout = config.get_int('koapy.context.server.terminate.timeout', 10)

        self._client = KiwoomOpenApiPlusServiceClient(port=self._port)

        self.logger.debug('Testing if client is ready...')
        if not self._client.is_ready(self._client_check_timeout):
            self.logger.debug('Client is not ready, creating a new server')
            self._server_proc = subprocess.Popen(self._server_proc_args)
            assert self._client.is_ready()
            self._stub = self._client.get_stub()
        else:
            self.logger.debug('Client is ready, using existing server')
            self._stub = self._client.get_stub()

        self._context_lock = threading.RLock()
        self._enter_count = 0

    def __del__(self):
        self.close_server_proc()

    def __enter__(self):
        with self._context_lock:
            self._enter_count += 1
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self._context_lock:
            if self._enter_count > 0:
                self._enter_count -= 1
                if self._enter_count == 0:
                    self.close()

    def get_stub(self):
        return self._stub

    def close_client(self):
        self._client.close()

    def close_server_proc(self):
        if self._server_proc is not None:
            self._server_proc.terminate() # maybe soft termination available via grpc? rather than hard termination
            self._server_proc.wait(self._server_proc_terminate_timeout)
            self._server_proc = None

    def close(self):
        self.close_client()
        self.close_server_proc()

    def __getattr__(self, name):
        try:
            stub = self.__getattribute__('_stub')
        except AttributeError:
            return self.__getattribute__(name)
        else:
            return getattr(stub, name)
