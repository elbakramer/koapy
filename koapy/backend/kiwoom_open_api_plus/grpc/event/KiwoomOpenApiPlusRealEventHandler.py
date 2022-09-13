import queue
import threading

from time import sleep

import grpc

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
    KiwoomOpenApiPlusRealType,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)
from koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedBufferedIterator import (
    QueueBasedBufferedIterator,
)
from koapy.utils.itertools import chunk
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusRealEventHandler(KiwoomOpenApiPlusEventHandlerForGrpc, Logging):

    _num_codes_per_screen = 100
    _default_opt_type = "0"

    def __init__(self, control, request, context, screen_manager):
        super().__init__(control, context)
        self._request = request
        self._screen_manager = screen_manager

        self._screen_no = request.screen_no
        self._code_list = request.code_list
        self._fid_list = request.fid_list
        self._opt_type = request.opt_type

        self._infer_fids = request.flags.infer_fids
        self._readable_names = request.flags.readable_names
        self._fast_parse = request.flags.fast_parse

        self._code_lists = [
            codes for codes in chunk(self._code_list, self._num_codes_per_screen)
        ]

        if len(self._screen_no) == 0:
            self._screen_nos = [None for i in range(len(self._code_lists))]
        elif len(self._screen_no) < len(self._code_lists):
            self.logger.warning("Given screen nos are not sufficient.")
            self._screen_nos = list(self._screen_no) + [
                None for i in range(len(self._code_lists) - len(self._screen_no))
            ]
        else:
            self._screen_nos = self._screen_no

        self._fid_list_joined = ";".join([str(fid) for fid in self._fid_list])
        self._opt_type_final = self._opt_type or self._default_opt_type

    def on_enter(self):
        for screen_no, code_list in zip(self._screen_nos, self._code_lists):
            code_list_joined = ";".join(code_list)
            screen_no = self._screen_manager.borrow_screen(screen_no)
            self.add_callback(self._screen_manager.return_screen, screen_no)
            for code in code_list:
                self.add_callback(
                    self.control.SetRealRemove.queuedCall, screen_no, code
                )
            KiwoomOpenApiPlusError.try_or_raise(
                self.control.SetRealReg.queuedCall(
                    screen_no,
                    code_list_joined,
                    self._fid_list_joined,
                    self._opt_type_final,
                ).result()
            )

    def OnReceiveRealData(self, code, realtype, realdata):
        if code in self._code_list:
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveRealData"
            response.arguments.add().string_value = code
            response.arguments.add().string_value = realtype
            response.arguments.add().string_value = realdata

            if self._infer_fids:
                fids = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(realtype)
            else:
                fids = self._fid_list

            if self._readable_names:
                names = [
                    KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid))
                    for fid in fids
                ]
            else:
                names = [str(fid) for fid in fids]

            if self._infer_fids and self._fast_parse:
                values = realdata.split("\t")
            else:
                values = [self.control.GetCommRealData(code, fid) for fid in fids]

            assert len(names) == len(values)

            response.single_data.names.extend(names)
            response.single_data.values.extend(values)

            self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        if errcode < 0:
            error = KiwoomOpenApiPlusNegativeReturnCodeError(errcode)
            self.observer.on_error(error)
            return


class KiwoomOpenApiPlusBidirectionalRealEventHandler(
    KiwoomOpenApiPlusRealEventHandler, Logging
):
    def __init__(self, control, request_iterator, context, screen_manager):
        request = KiwoomOpenApiPlusService_pb2.RealRequest()
        super().__init__(control, request, context, screen_manager)

        self._request_iterator = request_iterator
        self._buffered_request_iterator = QueueBasedBufferedIterator(
            self._request_iterator
        )

        self._fid_list = []
        self._fid_list_joined = ";".join(str(fid) for fid in self._fid_list)

        self._screen_by_code = {}
        self._code_list_by_screen = {}
        self._code_list = []

        self._request_iterator_consumer = None
        self._request_iterator_consumer_should_stop = False
        self._request_iterator_consumer_timeout = 2.0

    def register_code(self, code, fid_list=None):
        if code in self._screen_by_code:
            screen_no = self._screen_by_code[code]
            opt_type = "1"
        else:
            screen_no = None
            opt_type = "0"

            for (
                existing_screen_no,
                screen_code_list,
            ) in self._code_list_by_screen.items():
                if len(screen_code_list) < self._num_codes_per_screen:
                    screen_no = existing_screen_no
                    opt_type = "1"
                    break

            if screen_no is None:
                screen_no = self._screen_manager.borrow_screen()
                opt_type = "0"

            self._screen_by_code[code] = screen_no
            self._code_list_by_screen.setdefault(screen_no, []).append(code)
            self._code_list.append(code)

        if fid_list:
            fid_list_joined = ";".join(str(fid) for fid in fid_list)
        else:
            fid_list_joined = self._fid_list_joined

        self.logger.debug(
            "Registering code %s to screen %s with type %s", code, screen_no, opt_type
        )

        def try_to_register(retry=2, timeout=3.0):
            retry_count = 0

            def call():
                KiwoomOpenApiPlusError.try_or_raise(
                    self.control.SetRealReg.queuedCall(
                        screen_no, code, fid_list_joined, opt_type
                    ),
                    except_callback=on_error,
                )

            def on_error(e):
                nonlocal retry_count
                if isinstance(e, KiwoomOpenApiPlusError):
                    error_message = (
                        f"Failed to register {code=}. Reason: {e} ({e.code})."
                    )
                else:
                    error_message = f"Failed to register {code=}. Reason: {e}."
                if retry_count < retry:
                    retry_count += 1
                    self.logger.warning(
                        f"{error_message} Retrying ({retry_count}/{retry}) in {timeout} ..."
                    )
                else:
                    self.logger.warning(
                        f"{error_message} Kiwoom server does not allow register."
                    )
                    return
                sleep(timeout)
                call()

            call()

        try_to_register()

    def remove_code(self, code):
        if code in self._screen_by_code:
            screen_no = self._screen_by_code[code]
            self.logger.debug("Removing code %s from screen %s", code, screen_no)
            self.control.SetRealRemove.queuedCall(screen_no, code)
            self._screen_by_code.pop(code)
            self._code_list_by_screen[screen_no].remove(code)
            self._code_list.remove(code)
        else:
            self.logger.warning(
                "Given code %s is not in managed code list and cannot be removed", code
            )

    def remove_all_codes(self):
        code_list = list(
            self._code_list
        )  # copy in order to prevent "modification while iteration"
        for code in code_list:
            self.remove_code(code)

    def remove_all_screens(self):
        self.remove_all_codes()
        screen_nos = list(self._code_list_by_screen.keys())
        for screen_no in screen_nos:
            self.control.DisconnectRealData(
                screen_no
            )  # ensure although already removed in remove_all_codes()
            self._screen_manager.return_screen(screen_no)
            code_list = self._code_list_by_screen.pop(screen_no)
            assert len(code_list) == 0

    def consume_request_iterator(self):
        while not self._request_iterator_consumer_should_stop:
            try:
                request = self._buffered_request_iterator.next(
                    timeout=self._request_iterator_consumer_timeout
                )
            except queue.Empty:
                pass
            except grpc.RpcError:
                break
            else:
                if request.HasField("register_request"):
                    code_list = request.register_request.code_list
                    fid_list = request.register_request.fid_list
                    for code in code_list:
                        self.register_code(code, fid_list)
                elif request.HasField("remove_request"):
                    code_list = request.remove_request.code_list
                    for code in code_list:
                        self.remove_code(code)
                elif request.HasField("stop_request"):
                    self.stop()
                    break
                elif request.HasField("initialize_request"):
                    self._fid_list = request.initialize_request.fid_list
                    self._fid_list_joined = ";".join(str(fid) for fid in self._fid_list)
                    self._infer_fids = request.initialize_request.flags.infer_fids
                    self._infer_fids = True
                    self._readable_names = (
                        request.initialize_request.flags.readable_names
                    )
                    self._fast_parse = request.initialize_request.flags.fast_parse
                    self.remove_all_codes()
                else:
                    raise KiwoomOpenApiPlusError("Unexpected request")

    def stop_request_iterator_consumer(self):
        if (
            self._request_iterator_consumer is not None
            and self._request_iterator_consumer.is_alive()
        ):
            self._request_iterator_consumer_should_stop = True
            self._request_iterator_consumer.join()

    def start_request_iterator_consumer(self):
        self.stop_request_iterator_consumer()
        self._request_iterator_consumer_should_stop = False
        self._request_iterator_consumer = threading.Thread(
            target=self.consume_request_iterator, daemon=True
        )
        self._request_iterator_consumer.start()

    def on_enter(self):
        self.start_request_iterator_consumer()

    def on_exit(self, exc_type=None, exc_value=None, traceback=None):
        self.stop_request_iterator_consumer()
        self.remove_all_screens()

    def OnReceiveRealData(self, code, realtype, realdata):
        if code in self._code_list:
            response = KiwoomOpenApiPlusService_pb2.ListenResponse()
            response.name = "OnReceiveRealData"
            response.arguments.add().string_value = code
            response.arguments.add().string_value = realtype
            response.arguments.add().string_value = realdata

            if self._infer_fids:
                fids = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(realtype)
            else:
                fids = self._fid_list

            if self._readable_names:
                names = [
                    KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid))
                    for fid in fids
                ]
            else:
                names = [str(fid) for fid in fids]

            if self._infer_fids and self._fast_parse:
                values = realdata.split("\t")
            else:
                values = [self.control.GetCommRealData(code, fid) for fid in fids]

            assert len(names) == len(values)

            response.single_data.names.extend(names)
            response.single_data.values.extend(values)

            self.observer.on_next(response)
