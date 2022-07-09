from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandler import (
    KiwoomOpenApiPlusEventHandler,
)


class KiwoomOpenApiPlusEventHandlerForGrpc(KiwoomOpenApiPlusEventHandler):
    def __init__(self, control, context):
        super().__init__(control)

        self._context = context
        self._context.add_callback(self.stop)

    @property
    def context(self):
        return self._context
