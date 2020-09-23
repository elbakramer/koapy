=====
Usage
=====

Python
------

To use KOAPY in a project::

    import koapy

CLI
---

To use KOAPY in a CLI:

.. code-block:: console

    $ koapy
    Usage: koapy [OPTIONS] COMMAND [ARGS]...

    Options:
      -V, --version  Show the version and exit.
      -h, --help     Show this message and exit.

    Commands:
      config  Configure many things.
      get     Get various types of data.
      login   Ensure logged in when server is up.
      order   Place an order.
      serve   Start grpc server with tray application.
      update  Update openapi metadata.
      watch   Watch realtime data.

Python (More)
-------------

KOAPY 를 사용하지 않고 작성한 가장 미니멀한 코드 예시가 다음과 같을때,

.. literalinclude:: ../koapy/examples/roll_your_own.py
    :language: python

이것을 KOAPY 에서는 아래처럼 제공하고 있습니다.
하지만 KOAPY 에서는 이것보다 좀 더 상위의 API 를 제공하고 있기 때문에 사실 굳이 이렇게 사용할 필요는 없습니다.

.. literalinclude:: ../koapy/examples/lower_access.py
    :language: python

예시를 좀 더 복잡하게 해서, 로그인 후 특정 종목의 현재가를 가져오는 시나리오를 가정했을때,
만약 이것을 직접 짜는 경우에는 다음처럼 됩니다.

.. literalinclude:: ../koapy/examples/roll_your_own_event.py
    :language: python

이벤트 처리를 위해서 ``QEventLoop`` 을 생성하여 이벤트가 들어올 구간에 맞게 실행/종료를 시켜야 하며,
이벤트를 직접적으로 처리할 콜백 함수들도 알맞게 구현후 적절한 타이밍에 ``connect``/``disconnect`` 시켜주어야 합니다.

반면에 KOAPY 를 사용하면 동일한 작업을 아래와 같이 미리 주어진 메서드 (``GetStockInfoAsDataFrame``) 를 사용해 간단하게 처리가 가능합니다.
좀 더 세부적인 컨트롤이 필요할 경우에는 요청할 TR 에 대한 정보를 직접 설정하고 주어진 API (``TransactionCall``) 를 통해 호출한 뒤에
반환되는 스트림을 순차적으로 처리하는 식으로 구현이 가능합니다. 앞선 이벤트루프/콜백함수 기반 구현과 비교했을때 이 방식이 좀 더 직관적입니다.

.. literalinclude:: ../koapy/examples/transaction_event.py
    :language: python

``KiwoomOpenApiContext`` 객체를 통해 사용 가능한 메서드 목록은 기본적으로 개발가이드_ 에서 제공하는 모든 메서드들에서 시작합니다.
이후 그런 기본 메서드를 활용하는 상위함수들이 구현된 여러 래퍼 클래스들이 단계적으로 적용되면서
최종적으로 완성이 되는 구조입니다. 따라서 해당 래퍼 클래스들의 구현을 모두 참고하시는게 좋습니다.

주요 래퍼 클래스들을 고르자면 다음과 같습니다.

* :mod:`koapy.pyqt5.KiwoomOpenApiControlWrapper`
* :mod:`koapy.grpc.KiwoomOpenApiServiceClientStubWrapper`

여기서의 함수들 중에 ``XXXCall`` 패턴의 함수들에는 몇몇 유형화가 가능한 사용 패턴들에 대한 이벤트 처리 로직들이 미리 구현되어 있습니다.
혹시나 추후에 이런 메서드들이 다루지 못하는 새로운 사용 패턴이 생기는 경우에
기존 구현들을 참고해 커스텀 ``EventHandler`` 를 개발 후 ``CustomCallAndListen`` 을 활용하거나
아예 ``KiwoomOpenApiService.proto`` 파일을 수정해 신규 gRPC 메서드를 추가하는 방식으로도 확장이 가능합니다.

관련해서 참고할만한 클래스/모듈들입니다.

* :mod:`koapy.grpc.KiwoomOpenApiServiceServicer`
* :mod:`koapy.grpc.event.KiwoomOpenApiEventHandler`

아래는 최상단의 ``KiwoomOpenApiContext`` 부터 최하단의 ``KiwoomOpenApiQAxWidget`` 어떠한 흐름으로 이어져있는지 도식화한 것입니다.

.. code-block::

    KiwoomOpenApiContext
    ->KiwoomOpenApiServiceClientStubWrapper
    ->KiwoomOpenApiServiceClientStubCoreWrapper
    ->KiwoomOpenApiServiceStub
    ->KiwoomOpenApiServiceClient
    <=>
    ->KiwoomOpenApiServiceServer
    ->KiwoomOpenApiServiceServicer
    ->KiwoomOpenApiControlWrapper
    ->KiwoomOpenApiQAxWidget

.. _개발가이드: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf

CLI (More)
----------

CLI 는 아무 옵션없이 ``koapy`` 명령어만 실행했을때 출력되는 설명문을 먼저 참고하세요.
이후 필요한 커맨드를 정하고 ``--help`` 옵션을 통해 다른 옵션을 어떻게 설정하는지 확인하셔서
최종적으로 알맞게 옵션을 설정해 호출/사용하는 흐름으로 활용하시면 됩니다.

.. code-block:: console

    $ koapy
    Usage: koapy [OPTIONS] COMMAND [ARGS]...

    Options:
      -V, --version  Show the version and exit.
      -h, --help     Show this message and exit.

    Commands:
      config  Configure many things.
      get     Get various types of data.
      login   Ensure logged in when server is up.
      order   Place an order.
      serve   Start grpc server with tray application.
      update  Update openapi metadata.
      watch   Watch realtime data.

.. code-block:: console

    $ koapy get
    Usage: koapy get [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --help  Show this message and exit.

    Commands:
      daily       Get daily OHLCV of stocks.
      deposit     Get account deposit.
      errmsg      Get error message for error code.
      evaluation  Get account evaluation.
      holidays    Get market holidays.
      minute      Get minute OHLCV of stocks.
      modulepath  Get OpenApi module installation path.
      orders      Get order history of a date.
      realinfo    Get real type info.
      stockcode   Get stock codes.
      stockinfo   Get basic information of stocks.
      stockname   Get name for stock codes.
      trinfo      Get TR info.
      userinfo    Get user information.

.. code-block:: console

    $ koapy get stockinfo
    Usage: koapy get stockinfo [OPTIONS]

      Possible market codes are:
        0 : 장내
        10 : 코스닥
        3 : ELW
        8 : ETF
        50 : KONEX
        4 : 뮤추얼펀드
        5 : 신주인수권
        6 : 리츠
        9 : 하이얼펀드
        30 : K-OTC

      Possible market code aliases are:
        all: All possible market codes.

    Options:
      -c, --code CODE        Stock code to get. Can set multiple times.
      -m, --market MARKET    Stock market code to get. Alternative to --code. Can
                            set multiple times.

      -i, --input FILENAME   Text or excel file containing codes. Alternative to
                            --code or --market.

      -o, --output FILENAME  Output filename. Optional for single code (prints to
                            console).

      -p, --port PORT        Port number of grpc server (optional).
      -v, --verbose          Verbosity.
      -h, --help             Show this message and exit.

.. code-block:: console

    $ koapy get stockinfo -c 005930
    |                 | 0        |
    |:----------------|:---------|
    | 종목코드        | 005930   |
    | 종목명          | 삼성전자 |
    | 결산월          | 12       |
    | 액면가          | 100      |
    | 자본금          | 7780     |
    | 상장주식        | 5969783  |
    | 신용비율        | +0.10    |
    | 연중최고        | +62800   |
    | 연중최저        | -42300   |
    | 시가총액        | 3498293  |
    | 시가총액비중    |          |
    | 외인소진률      | 0.00     |
    | 대용가          | 46880    |
    | PER             | 18.51    |
    | EPS             | 3166     |
    | ROE             | 8.7      |
    | PBR             | 1.56     |
    | EV              | 4.52     |
    | BPS             | 37528    |
    | 매출액          | 2304009  |
    | 영업이익        | 277685   |
    | 당기순이익      | 217389   |
    | 250최고         | +62800   |
    | 250최저         | -42300   |
    | 시가            | 0        |
    | 고가            | 0        |
    | 저가            | 0        |
    | 상한가          | +76100   |
    | 하한가          | -41100   |
    | 기준가          | 58600    |
    | 예상체결가      | -0       |
    | 예상체결수량    | 0        |
    | 250최고가일     | 20200120 |
    | 250최고가대비율 | -6.69    |
    | 250최저가일     | 20200319 |
    | 250최저가대비율 | +38.53   |
    | 현재가          | 58600    |
    | 대비기호        | 3        |
    | 전일대비        | 0        |
    | 등락율          | 0.00     |
    | 거래량          | 0        |
    | 거래대비        | 0.00     |
    | 액면가단위      | 원       |
    | 유통주식        | 4450781  |
    | 유통비율        | 74.6     |

CLI 는 명령을 실행할때마다 매번 프로그램이 새로 실행되는 식이기 때문에
단순히 명령을 여러번 연이어 실행하는 경우 (자동 로그인을 설정해두었더라도) 매번 로그인을 수행해야하는 번거로움이 있을 수 있습니다.

이런 경우 별도 프로세스로 gRPC 서버를 미리 띄워둔 뒤에 다른 창에서 CLI 명령을 실행하게되면,
최초 로그인 이후의 명령들은 이미 로그인된 서버와 통신하여 명령을 수행하게 되면서 불필요한 로그인 단계를 줄일 수 있습니다.

.. code-block:: console

    (server) $ koapy serve
    2020-09-24 06:02:55,028 [DEBUG] Starting app -- KiwoomOpenApiTrayApplication.py:176
    2020-09-24 06:02:55,029 [DEBUG] Starting server -- KiwoomOpenApiTrayApplication.py:177
    2020-09-24 06:02:55,031 [DEBUG] Started server -- KiwoomOpenApiTrayApplication.py:182

.. code-block:: console

    (client) $ koapy login
    Logging in...
    Logged into Simulation server.

.. code-block:: console

    (server) $ ...
    2020-09-24 06:02:55,031 [DEBUG] Started server -- KiwoomOpenApiTrayApplication.py:182

    [GetPCIdentity] VER 3.2.0.0  build 2015.8.12

    [GetPCIdentity] VER 3.2.0.0  build 2015.8.12
    2020-09-24 06:03:17,144 [DEBUG] OnEventConnect(0) -- KiwoomOpenApiEventHandler.py:73
    2020-09-24 06:03:17,145 [DEBUG] Connected to server -- KiwoomOpenApiTrayApplication.py:108

.. code-block:: console

    (client) $ koapy get stockinfo -c 005930
    ...

.. code-block:: console

    (server) $ ...
    2020-09-24 06:03:17,145 [DEBUG] Connected to server -- KiwoomOpenApiTrayApplication.py:108
    2020-09-24 06:03:48,742 [DEBUG] CommRqData() was successful; CommRqData('주식기본정보요청', 'opt10001', 0, '0291') with inputs {'종목코드': '005930'} -- KiwoomOpenApiControlWrapper.py:151
    2020-09-24 06:03:48,756 [DEBUG] OnReceiveTrData('0291', '주식기본정보요청', 'opt10001', '', '0') -- KiwoomOpenApiEventHandler.py:17
