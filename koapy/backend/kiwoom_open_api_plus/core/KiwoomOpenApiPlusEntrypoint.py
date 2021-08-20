import subprocess
import threading

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypointMixin import (
    KiwoomOpenApiPlusEntrypointMixin,
)
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClient import (
    KiwoomOpenApiPlusServiceClient,
)
from koapy.config import config, get_32bit_executable
from koapy.utils.logging import get_verbosity
from koapy.utils.logging.Logging import Logging
from koapy.utils.networking import get_free_localhost_port


class KiwoomOpenApiPlusEntrypoint(KiwoomOpenApiPlusEntrypointMixin, Logging):
    def __init__(
        self,
        port=None,
        client_check_timeout=None,
    ):
        if port is None:
            port = (
                config.get("koapy.backend.kiwoom_open_api_plus.grpc.port", 0)
                or get_free_localhost_port()
            )

        self._port = port
        self._client_check_timeout = client_check_timeout

        self._server_executable = get_32bit_executable()
        self._server_proc_args = [self._server_executable, "-m", "koapy.cli", "serve"]
        if self._port is not None:
            self._server_proc_args.extend(["-p", str(self._port)])

        self._verbosity = get_verbosity()
        self._server_proc_args.extend(["-" + "v" * self._verbosity])

        self._server_proc = None
        self._server_proc_start_timeout = 30
        self._server_proc_terminate_timeout = 30

        self._client = KiwoomOpenApiPlusServiceClient(port=self._port)

        self.logger.debug("Testing if client is ready...")
        if not self._client.is_ready(self._client_check_timeout):
            self.logger.debug("Client is not ready")
            self.logger.debug("Creating a new server...")
            self._server_proc = subprocess.Popen(self._server_proc_args)
            assert self._client.is_ready(
                self._server_proc_start_timeout
            ), "Failed to create server"
            self._stub = self._client.get_stub()
        else:
            self.logger.debug("Client is ready, using existing server")
            self._stub = self._client.get_stub()

        self._context_lock = threading.RLock()
        self._enter_count = 0

    def __del__(self):
        self.close()

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
            self._server_proc.terminate()  # maybe soft termination available via grpc? rather than hard termination
            self._server_proc.wait(self._server_proc_terminate_timeout)
            self._server_proc = None

    def close(self):
        self.close_client()
        self.close_server_proc()

    def __getattr__(self, name):
        try:
            stub = self.__getattribute__("_stub")
        except AttributeError:
            return self.__getattribute__(name)
        else:
            return getattr(stub, name)
