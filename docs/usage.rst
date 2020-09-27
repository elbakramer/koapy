=====
Usage
=====

Python
------

To use KOAPY in a project::

    import koapy

CLI
---

To use KOAPY in a command line:

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

KOAPY 를 사용하지 않고 작성한 가장 미니멀한 코드 예시가 다음과 같을 때:

.. literalinclude:: ../koapy/examples/roll_your_own.py
    :language: python

이것을 KOAPY 에서는 아래처럼 제공하고 있습니다:

.. literalinclude:: ../koapy/examples/lower_access.py
    :language: python

전체적인 구조에서 큰 차이는 없고, 차이점이라면 함수 호출시 |dynamicCall|_ 함수를 사용하지 않고
직접적으로 함수를 호출하고 있다는 점입니다.

당장 이렇게 사용할 수도 있겠지만 KOAPY 에서는 이것보다 좀 더 상위의 API 를 제공하고 있기 때문에,
직접 하위 API 를 통해서 컨트롤 할 것이 아니라면 굳이 이렇게 사용할 필요는 없습니다.

예시를 좀 더 복잡하게 해서, 로그인 후 특정 종목의 현재가를 가져오는 시나리오를 가정했을때,
만약 이것을 KOAPY 없이 직접 짜는 경우에는 다음처럼 됩니다:

.. literalinclude:: ../koapy/examples/roll_your_own_event.py
    :language: python

단순 함수콜에 비해서 추가된 점들을 짚어보면,
이벤트 처리를 위하여 |QEventLoop|_ 를 생성하여 이벤트가 들어올 구간에 맞게 실행/종료를 시키고 있으며,
이벤트를 직접적으로 처리할 콜백 함수들도 알맞게 구현후 적절한 타이밍에 |connect|_/|disconnect|_ 하고 있습니다.

반면에 KOAPY 를 사용하면 동일한 작업을 아래와 같이 미리 주어진 메서드 :py:meth:`~.koapy.grpc.KiwoomOpenApiServiceClientStubWrapper.KiwoomOpenApiServiceClientStubWrapper.GetStockInfoAsDataFrame`) 를 사용해 간단하게 처리가 가능합니다.
좀 더 세부적인 컨트롤이 필요할 경우에는 요청할 TR 에 대한 정보를 직접 설정하고 중간단계의 API (:py:meth:`~.koapy.grpc.KiwoomOpenApiServiceClientStubWrapper.KiwoomOpenApiServiceClientStubCoreWrapper.TransactionCall`) 를 통해 호출한 뒤에
반환되는 스트림을 순차적으로 처리하는 식으로 구현이 가능합니다.
앞선 이벤트루프/콜백함수 기반 구현과 비교했을 때 이 방식이 좀 더 직관적입니다.

.. |dynamicCall| replace:: ``dynamicCall``
.. _dynamicCall: https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qaxcontainer/qaxbase.html?highlight=dynamicCall#dynamicCall
.. |QEventLoop| replace:: ``QEventLoop``
.. _QEventLoop: https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtcore/qeventloop.html

.. |connect| replace:: ``connect``
.. _connect: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html?highlight=connect#connect
.. |disconnect| replace:: ``disconnect``
.. _disconnect: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html?highlight=disconnect#disconnect

.. literalinclude:: ../koapy/examples/transaction_event.py
    :language: python

:py:class:`~.koapy.context.KiwoomOpenApiContext.KiwoomOpenApiContext` 객체를 통해 사용 가능한 메서드 목록은 기본적으로 OpenAPI 에서 제공하는 모든 메서드들을 기반으로 합니다.
해당 메서드 목록은 `키움 OpenAPI+ 개발 가이드 문서`_ 에서 확인 가능합니다.

.. _`키움 OpenAPI+ 개발 가이드 문서`: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf#page=12

이후 그런 기본 메서드들을 활용하는 상위 함수들이 구현된 여러 래퍼 클래스들이 단계적으로 적용되면서
최종적으로 모든 메서드들이 :py:class:`~.koapy.context.KiwoomOpenApiContext.KiwoomOpenApiContext` 객체로 합쳐지는 구조입니다.
따라서 해당 메서드들이 어떤 것들이 있는지 확인하기 위해서는 관련 래퍼 클래스들에 구현된 함수들을 참고하시는 게 좋습니다.

주요 래퍼 클래스들을 포함하는 모듈들은 다음과 같습니다.

* :py:mod:`koapy.pyqt5.KiwoomOpenApiControlWrapper`
* :py:mod:`koapy.grpc.KiwoomOpenApiServiceClientStubWrapper`

여기서의 함수들 중에 ``XXXCall`` 패턴의 함수들은 TR/실시간 데이터 처리 등 몇몇 유형화가 가능한 사용 패턴들에 대해서
미리 구현해놓은 이벤트 처리 로직들이 서버 사이드에서 동작하도록 구성되어 있습니다.
혹시나 추후에 이런 메서드들이 다루지 못하는 새로운 사용 패턴이 생기는 경우에
기존 구현들을 참고해 커스텀 :py:mod:`EventHandler<koapy.grpc.event.KiwoomOpenApiEventHandler>` 를 개발 후 :py:meth:`~.koapy.grpc.KiwoomOpenApiServiceServicer.KiwoomOpenApiServiceServicer.CustomCallAndListen` 을 활용하거나
아예 |KiwoomOpenApiService.proto|_ 파일을 수정해 신규 gRPC 메서드를 추가하는 방식으로도 확장이 가능합니다.

.. |KiwoomOpenApiService.proto| replace:: ``KiwoomOpenApiService.proto``
.. _`KiwoomOpenApiService.proto`: https://github.com/elbakramer/koapy/blob/master/koapy/grpc/KiwoomOpenApiService.proto

서버 사이드의 이벤트 처리와 관련해서 참고할만한 모듈들입니다.

* :py:mod:`koapy.grpc.KiwoomOpenApiServiceServicer`
* :py:mod:`koapy.grpc.event.KiwoomOpenApiEventHandler`

아래는 전체적으로 최상단의 :py:class:`~.koapy.context.KiwoomOpenApiContext.KiwoomOpenApiContext` 부터
최하단의 :py:class:`~.koapy.pyqt5.KiwoomOpenApiQAxWidget.KiwoomOpenApiQAxWidget` 까지
어떠한 흐름으로 이어져있는지 도식화한 것입니다.

.. code-block::

    KiwoomOpenApiContext
    -> KiwoomOpenApiServiceClientStubWrapper + KiwoomOpenApiServiceClientStubCoreWrapper + KiwoomOpenApiControlCommonWrapper
    -> KiwoomOpenApiServiceStub
    -> KiwoomOpenApiServiceClient
    <=gRPC=>
    -> KiwoomOpenApiServiceServer
    -> KiwoomOpenApiServiceServicer + KiwoomOpenApiEventHandler
    -> KiwoomOpenApiControlWrapper + KiwoomOpenApiControlCommonWrapper
    -> KiwoomOpenApiQAxWidget

CLI (More)
----------

CLI 는 KOAPY 설치 후 아무 옵션 없이 ``koapy`` 명령어만 실행했을 때 출력되는 설명문을 먼저 참고하세요.
이후 필요한 커맨드를 정하고 ``--help`` 옵션을 통해 다른 옵션을 어떻게 설정하는지 확인하신 뒤
최종적으로 옵션을 알맞게 설정해 호출, 사용하는 흐름으로 활용하시면 됩니다.

Auto login
==========

만약에 최초로 사용하시는 경우에는 자동 로그인 설정부터 해놓는 것을 추천드립니다.

.. code-block:: console

    $ koapy config autologin

위의 명령어 실행시 키움 Open API 로그인 창이 뜰겁니다.

입력창 아래의 ``고객 아이디 저장`` 을 체크해서 매번 아이디를 입력하지 않도록 합니다.
그리고 실제 사용이 아닌 테스트 목적이므로 ``모의투자 접속`` 을 체크합니다.
참고로 모의투자로 접속하려면 `상시 모의투자`_ 를 신청해놓은 상태여야 합니다.

.. _`상시 모의투자`: https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1101000000

이후 고객ID 와 비밀번호를 입력하고 로그인을 진행합니다.

만약에 업데이트로 인해 탑재 프로그램을 종료하고 확인 버튼을 누르라는 메시지가 뜨는 경우에
터미널에서 CTRL+C 로 현재 프로세스를 종료시키거나 아예 터미널을 닫은 뒤 확인 버튼을 누르시면 정상적으로 업데이트가 진행됩니다.

로그인이 완료되면 이어서 계좌 비밀번호 입력 화면이 뜰겁니다.
여기서 각 계좌의 계좌번호를 입력하고 ``등록`` 버튼을 누릅니다.
모의투자의 경우는 모든 계좌의 비밀번호가 ``0000`` 이므로 ``0000`` 을 입력하고 ``전체 계좌에 등록`` 버튼을 누릅니다.
마지막으로 아래의 ``AUTO`` 박스를 체크하고 창을 닫습니다.
이제 이후부터는 로그인 단계에서 사용자 입력을 묻지 않고 자동으로 로그인이 처리됩니다.

Uasge example
=============

아래는 예시로 맨 처음 커멘드 목록의 커멘드들 중에 ``get`` 커멘드를 확인하고 따라가서
최종적으로 주식기본정보 확인 기능을 사용하는 시나리오입니다.

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

gRPC server
===========

CLI 는 명령을 실행할 때마다 매번 프로그램이 새로 실행되는 식이기 때문에
단순히 명령을 여러 번 연이어 실행하는 경우 (자동 로그인을 설정해두었더라도) 매번 로그인을 수행해야 하는 번거로움이 있을 수 있습니다.

이런 경우 별도 프로세스로 gRPC 서버를 미리 띄워둔 뒤에 다른 창에서 CLI 명령을 실행하게 되면,
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

Tray icon
---------

KOAPY 가 동작하는 동안 내부적으로 :py:class:`~.koapy.pyqt5.KiwoomOpenApiTrayApplication.KiwoomOpenApiTrayApplication` 이 구동되며
이것을 직접 확인할 수 있도록 구동되는 동안 우측하단에 트레이 아이콘을 표시하게끔 구현되어있습니다.
아직 따로 마땅한 아이콘이 없어서 초록색 바탕에 ``Qt`` 가 적혀있는 디폴트 아이콘이 그것입니다.

이것을 가장 빠르게 확인할 수 있는 방법은 서버를 띄워보는 것입니다.

.. code-block:: console

    $ koapy serve

해당 트레이 아이콘을 우클릭하는 경우 아래와 같은 여러 기능들을 수행할 수 있는 메뉴를 제공합니다.

* 로그인 처리
* 자동 로그인 설정
* 로그인 여부 확인
* 접속중인 서버 타입 확인
* 각종 관련 외부링크
* 어플리케이션 종료

해당 트레이 아이콘을 더블클릭하는 경우 :py:class:`~.koapy.pyqt5.KiwoomOpenApiQAxWidget.KiwoomOpenApiQAxWidget` 에 대응되는 위젯이 뜨는데
현재로는 크게 의미있는 요소를 넣거나 한 것은 없어서 그냥 닫으시면 됩니다.
