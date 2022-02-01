=====
KOAPY
=====

.. container::

    .. image:: https://img.shields.io/pypi/v/koapy.svg
            :target: https://pypi.python.org/pypi/koapy
            :alt: PyPI Version

    .. image:: https://img.shields.io/pypi/pyversions/koapy.svg
            :target: https://pypi.python.org/pypi/koapy/
            :alt: PyPI Python Versions

    .. image:: https://img.shields.io/pypi/status/koapy.svg
            :target: https://pypi.python.org/pypi/koapy/
            :alt: PyPI Status

    .. badges from below are commendted out

    .. .. image:: https://img.shields.io/pypi/dm/koapy.svg
            :target: https://pypi.python.org/pypi/koapy/
            :alt: PyPI Monthly Donwloads

.. container::

    .. image:: https://img.shields.io/github/workflow/status/elbakramer/koapy/CI/master
            :target: https://github.com/elbakramer/koapy/actions/workflows/ci.yml
            :alt: CI Build Status
    .. .. image:: https://github.com/elbakramer/koapy/actions/workflows/ci.yml/badge.svg?branch=master

    .. image:: https://img.shields.io/github/workflow/status/elbakramer/koapy/Documentation/master?label=docs
            :target: https://elbakramer.github.io/koapy/
            :alt: Documentation Build Status
    .. .. image:: https://github.com/elbakramer/koapy/actions/workflows/documentation.yml/badge.svg?branch=master

    .. image:: https://img.shields.io/codecov/c/github/elbakramer/koapy.svg
            :target: https://codecov.io/gh/elbakramer/koapy
            :alt: Codecov Coverage
    .. .. image:: https://codecov.io/gh/elbakramer/koapy/branch/master/graph/badge.svg

    .. image:: https://img.shields.io/requires/github/elbakramer/koapy/master.svg
            :target: https://requires.io/github/elbakramer/koapy/requirements/?branch=master
            :alt: Requires.io Requirements Status
    .. .. image:: https://requires.io/github/elbakramer/koapy/requirements.svg?branch=master

    .. badges from below are commendted out

    .. .. image:: https://img.shields.io/travis/elbakramer/koapy.svg
            :target: https://travis-ci.com/elbakramer/koapy
            :alt: Travis CI Build Status
    .. .. image:: https://travis-ci.com/elbakramer/koapy.svg?branch=master

    .. .. image:: https://img.shields.io/readthedocs/koapy/latest.svg
            :target: https://koapy.readthedocs.io/en/latest/?badge=latest
            :alt: ReadTheDocs Documentation Build Status
    .. .. image:: https://readthedocs.org/projects/koapy/badge/?version=latest

    .. .. image:: https://pyup.io/repos/github/elbakramer/koapy/shield.svg
            :target: https://pyup.io/repos/github/elbakramer/koapy/
            :alt: PyUp Updates

.. container::

    .. image:: https://img.shields.io/pypi/l/koapy.svg
            :target: https://github.com/elbakramer/koapy/blob/master/LICENSE
            :alt: PyPI License

    .. badges from below are commendted out

    .. .. image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Felbakramer%2Fkoapy.svg?type=shield
            :target: https://app.fossa.com/projects/git%2Bgithub.com%2Felbakramer%2Fkoapy?ref=badge_shield
            :alt: FOSSA Status

.. container::

    .. image:: https://badges.gitter.im/elbakramer/koapy.svg
            :target: https://gitter.im/koapy/community
            :alt: Gitter Chat
    .. .. image:: https://img.shields.io/gitter/room/elbakramer/koapy.svg

    .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
            :target: https://github.com/psf/black
            :alt: Code Style: Black


Kiwoom Open Api Plus Python

* Free software: `MIT`_ OR `Apache-2.0`_ OR `GPL-3.0-or-later`_
* Documentation: https://koapy.readthedocs.io.

.. _`MIT`: https://github.com/elbakramer/koapy/blob/master/LICENSE.MIT
.. _`Apache-2.0`: https://github.com/elbakramer/koapy/blob/master/LICENSE.APACHE-2.0
.. _`GPL-3.0-or-later`: https://github.com/elbakramer/koapy/blob/master/LICENSE.GPL-3.0-OR-LATER


Features
--------

KOAPY 는 `키움증권의 OpenAPI+`_ 를 Python 에서 쉽게 사용할 수 있도록 만든 라이브러리 패키지 및 툴입니다.

키움에서 제공하는 OpenAPI+ 를 활용하는데 필요한 아래와 같은 지식들을 알지 못해도,
기본적인 Python 에 대한 지식만 어느 정도 있다면 쉽게 사용할 수 있도록 하는 것에 초점을 두었습니다.

* 키움에서 제공하는 OpenAPI+ 의 OCX 라이브러리 구조
* OCX 를 Python 에서 구동하기 위한 PyQt5_/PySide2_ 와 |QAxWidget|_ 생성
* 컨트롤에서 함수 호출을 위한 |dynamicCall|_ 함수 사용
* 이벤트 처리를 위해 적절한 |signal|_/|slot|_ 설정 및 처리

KOAPY 는 아래와 같은 기능을 제공합니다.

* PyQt5_/PySide2_ 를 기반한 GUI 환경에 얽매일 필요 없이 일반적인 라이브러리처럼 가져다 활용할 수 있습니다.
  CLI 형태로 쓸 수도 있고 이외에 다양한 곳에서도 쉽게 활용이 가능합니다.
* 컨트롤 함수 호출 시 명세에 적혀있는 형태 그대로 Python 함수였던 것처럼 호출이 가능합니다.
  이후는 KOAPY 가 유연하게 처리합니다.
  매번 명세에 맞게 |dynamicCall|_ 의 인자를 적어 넣거나, 모든 존재하는 함수에 대해 미리 래퍼 함수를 손 아프게 만들어놓을 필요가 없습니다.
* 이벤트 처리 및 비동기 프로그래밍에 익숙하지 않더라도 그보다 비교적 쉬운 인터페이스를 통해 관련 기능들을 활용할 수 있습니다.
  가장 간단한 로그인 처리부터 TR/실시간 데이터 처리, 그리고 주문처리까지 다양한 시나리오에 대한 기본 이벤트 처리 로직을 제공합니다.
* 주식 기본정보 요청부터 일봉/분봉 등 시세 데이터 확인 그리고 예수금/잔고 확인까지 일반적으로 자주 사용되는 기능들에 대해서
  미리 구현된 함수를 제공합니다. 함수 호출 결과 중 테이블성 정보들은 |pandas.DataFrame|_ 타입으로 제공해 이후 분석 및 처리가 유용하게끔 했습니다.
* TR 의 입력/출력 데이터 구조, 실시간 데이터별 FID 목록, 에러코드에 대한 설명문 등,
  개발하는 과정에서 필요한 여러 메타정보들을 언어 내 라이브러리에서 바로 조회 및 활용이 가능합니다.
  매번 매뉴얼_ 이나 KOAStudio_ 를 열어서 참고하고 이후 일일이 하나씩 하드코딩할 필요가 없습니다.
* 로컬 네트워크에서 gRPC_ 를 통한 서버-클라이언트 형태의 구성이 가능합니다.
  이를 통해 "라이브러리 호환성으로 인해 32bit 환경에서만 작업되어야 한다" 는 제약을 벗어나 클라이언트는 Python 64bit 를 사용할 수도 있습니다.
  더 나아가서는 gRPC_ 에서 지원하는 모든 다양한 언어를 클라이언트로 작성해 사용하는 방식으로도 확장 가능합니다.
* 이외에 메시징/알람 기능, 휴장일 확인, TR 호출 시 호출 횟수 제한 회피 등 개발 및 활용에 필요한 다양한 부가기능들을 추가로 제공합니다.
* 굳이 Python 코드를 작성하지 않더라도 기본적인 기능들을 활용해볼 수 있도록 여러 커맨드를 포함하는 CLI 를 제공합니다.
  CLI 를 활용하면 마켓별 코드 목록 확인, 주식 기본정보 확인, 일봉/분봉 데이터 확인 및 저장, 실시간 데이터 구독 등
  다양한 기능들을 코드 구현 없이 사용할 수 있습니다. 서버도 CLI 커맨드로 쉽게 띄울 수 있습니다.

아래는 KOAPY 를 활용하는 예시 스크립트 입니다:

..  .. literalinclude:: ../koapy/examples/6_main_scenario.py
            :language: python

.. code-block:: python

    # 로깅 설정
    import logging

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d',
        level=logging.DEBUG)

    # KOAPY 임포트
    from koapy import KiwoomOpenApiPlusEntrypoint

    # 1. 엔트리포인트 객체 생성
    entrypoint = KiwoomOpenApiPlusEntrypoint()

    # 모듈 경로 확인 (기본 함수 사용 예시)
    module_path = entrypoint.GetAPIModulePath()
    print(module_path)

    # 2. 로그인 예시
    logging.info('Logging in...')
    entrypoint.EnsureConnected()
    logging.info('Logged in.')

    # 3. 기본 함수 실행 예시

    # 접속 상태 확인 (기본 함수 호출 예시)
    logging.info('Checking connection status...')
    status = entrypoint.GetConnectState()
    logging.info('Connection status: %s', status)

    # 종목 리스트 확인 (기본 함수 호출 예시)
    logging.info('Getting stock codes and names...')
    codes = entrypoint.GetCodeListByMarketAsList('0')
    names = [entrypoint.GetMasterCodeName(code) for code in codes]

    # 위에서 가져온 정보로 삼성전자의 code 확인
    codes_by_name = dict(zip(names, codes))
    logging.info('Checking stock code of Samsung...')
    code = samsung_code = codes_by_name['삼성전자']
    logging.info('Code of Samsung: %s', code)

    # 4. TR 요청 예시

    # 상위 함수를 활용한 TR 요청 예시 (opt10001)
    logging.info('Getting basic info of Samsung...')
    info = entrypoint.GetStockBasicInfoAsDict(code)
    logging.info('Got basic info data (using GetStockBasicInfoAsDict):')
    print(info)

    # 상위 함수를 활용한 TR 요청 예시 (opt10081)
    logging.info('Getting daily stock data of Samsung...')
    data = entrypoint.GetDailyStockDataAsDataFrame(code)
    logging.info('Got daily stock data:')
    print(data)

    # 하위 함수를 사용한 TR 요청 예시 (opt10001)
    rqname = '주식기본정보요청'
    trcode = 'opt10001'
    screen_no = '0001'  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    inputs = {'종목코드': code}

    output = {}

    logging.info('Requesting data for request name: %s', rqname)
    for event in entrypoint.TransactionCall(rqname, trcode, screen_no, inputs):
        logging.info('Got event for request: %s', rqname)
        names = event.single_data.names
        values = event.single_data.values
        for name, value in zip(names, values):
            output[name] = value

    logging.info('Got basic info data (using TransactionCall):')
    print(output)

    # (디버깅을 위한) 이벤트 메시지 출력 함수
    from pprint import PrettyPrinter
    from google.protobuf.json_format import MessageToDict

    pp = PrettyPrinter()

    def pprint_event(event):
        pp.pprint(MessageToDict(event, preserving_proto_field_name=True))

    logging.info('Last event message was:')
    pprint_event(event)

    # TR 관련 메타정보 확인
    from koapy import KiwoomOpenApiPlusTrInfo

    logging.info('Checking TR info of opt10001')
    tr_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code('opt10001')

    logging.info('Inputs of opt10001:')
    print(tr_info.inputs)
    logging.info('Single outputs of opt10001:')
    print(tr_info.single_outputs)
    logging.info('Multi outputs of opt10001:')
    print(tr_info.multi_outputs)

    # 5. 조건검색 예시

    # 조건검색 설정 불러오기
    entrypoint.EnsureConditionLoaded()

    # 일반 조건검색 예시
    condition_name = '대형 저평가 우량주'

    logging.info('Getting stock codes with condition: %s', condition_name)
    codes, info = entrypoint.GetCodeListByCondition(condition_name, with_info=True)

    print(codes)
    print(info)

    # 실시간 조건검색 예시
    condition_name = '중소형 저평가주'

    logging.info('Start listening realtime condition stream...')
    stream = entrypoint.GetCodeListByConditionAsStream(condition_name)

    # 이벤트 스트림을 도중에 멈추기 위해서 threading.Timer 활용
    import threading

    def stop_listening_cond():
        logging.info('Stop listening realtime events...')
        stream.cancel()

    threading.Timer(10.0, stop_listening_cond).start() # 10초 이후에 gRPC 커넥션 종료하도록 설정

    # 이벤트 불러와서 출력처리
    import grpc

    try:
        for event in stream:
            pprint_event(event)
    except grpc.RpcError as e:
        pass

    # 6.주문처리 예시

    # 현재 시장이 열려 있는지 (주문이 가능한지) 확인하는 함수
    from pandas import Timestamp
    from exchange_calendars import get_calendar

    krx_calendar = get_calendar('XKRX')

    def is_currently_in_session():
        now = Timestamp.now(tz=krx_calendar.tz)
        previous_open = krx_calendar.previous_open(now).astimezone(krx_calendar.tz)
        next_close = krx_calendar.next_close(previous_open).astimezone(krx_calendar.tz)
        return previous_open <= now <= next_close

    # 주문처리 파라미터 설정
    first_account_no = entrypoint.GetFirstAvailableAccount()

    request_name = "삼성전자 1주 시장가 신규 매수"  # 사용자 구분명, 구분가능한 임의의 문자열
    screen_no = "0001"  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    account_no = first_account_no  # 계좌번호 10자리, 여기서는 계좌번호 목록에서 첫번째로 발견한 계좌번호로 매수처리
    order_type = 1  # 주문유형, 1 : 신규매수
    code = samsung_code  # 종목코드, 앞의 삼성전자 종목코드
    quantity = 1  # 주문수량, 1주 매수
    price = 0  # 주문가격, 시장가 매수는 가격설정 의미없음
    quote_type = "03"  # 거래구분, 03 : 시장가
    original_order_no = ""  # 원주문번호, 주문 정정/취소 등에서 사용

    # 현재는 기본적으로 주문수량이 모두 소진되기 전까지 이벤트를 듣도록 되어있음 (단순 호출 예시)
    if is_currently_in_session():
        logging.info('Sending order to buy %s, quantity of 1 stock, at market price...', code)
        for event in entrypoint.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no):
            pprint_event(event)
    else:
        logging.info('Cannot send an order while market is not open, skipping...')

    # 7. 실시간 데이터 처리 예시
    from koapy import KiwoomOpenApiPlusRealType

    code_list = [code]
    fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name('주식시세')
    opt_type = '0' # 기존 화면에 추가가 아니라 신규 생성

    # 현재는 기본적으로 실시간 이벤트를 무한정 가져옴 (커넥션 컨트롤 가능한 예시)
    logging.info('Starting to get realtime stock data for code: %s', code)
    stream = entrypoint.GetRealDataForCodesAsStream(
        code_list,
        fid_list,
        opt_type,
        screen_no=None,  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
        infer_fids=True,  # True 로 설정 시 주어진 fid_list 를 고집하지 말고 이벤트 처리 함수의 인자로 전달받는 실시간데이터 이름에 따라 유연하게 fid_list 를 추론
        readable_names=True,  # True 로 설정 시 각 fid 마다 숫자 대신 읽을 수 있는 이름으로 변환하여 반환
        fast_parse=False,  # True 로 설정 시 이벤트 처리 함수내에서 데이터 값 읽기 시 GetCommRealData() 함수 호출 대신, 이벤트 처리 함수의 인자로 넘어오는 데이터를 직접 활용, infer_fids 가 True 로 설정된 경우만 유의미함
    )

    # 이벤트 스트림을 도중에 멈추기 위해서 threading.Timer 활용
    import threading

    def stop_listening_real():
        logging.info('Stop listening realtime events...')
        stream.cancel()

    threading.Timer(10.0, stop_listening_real).start() # 10초 이후에 gRPC 커넥션 종료하도록 설정

    # 이벤트 불러와서 출력처리
    import grpc

    try:
        for event in stream:
            pprint_event(event)
    except grpc.RpcError as e:
        print(e)

    # 예시 스크립트 끝
    logging.info('End of example')

    # 리소스 해제
    entrypoint.close()


.. _`키움증권의 OpenAPI+`: https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000

.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt/
.. _PySide2: https://doc.qt.io/qtforpython/index.html
.. _매뉴얼: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf
.. _KOAStudio: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf#page=7
.. _gRPC: https://grpc.io/

.. |QAxWidget| replace:: ``QAxWidget``
.. _QAxWidget: https://doc.qt.io/qt-5/qaxwidget.html
.. |dynamicCall| replace:: ``dynamicCall``
.. _dynamicCall: https://doc.qt.io/qt-5/qaxbase.html#dynamicCall
.. |signal| replace:: ``signal``
.. _signal: https://doc.qt.io/qt-5/signalsandslots.html#signals
.. |slot| replace:: ``slot``
.. _slot: https://doc.qt.io/qt-5/signalsandslots.html#slots
.. |pandas.DataFrame| replace:: ``pandas.DataFrame``
.. _`pandas.DataFrame`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html


Installation
------------

해당 라이브러리는 PyPI_ 를 통해서 설치 가능합니다:

.. code-block:: console

    $ pip install koapy

만약에 기본 기능 이외에 추가적인 기능들을 사용하고자 하는 경우, 아래처럼 추가적인 의존성까지 같이 설치해주셔야 합니다.

예를 들어 backtrader_ 관련 기능들이 구현된 |koapy.backtrader|_ 모듈 하위의 기능들을 사용하고자 하는 경우,
관련 의존성을 포함해 설치하기 위해서는 아래와 같이 설치합니다:

.. code-block:: console

    $ pip install koapy[backtrader]

별개로 backtrader_ 와 관련해서는 Licensing_ 옵션과 관련해서 주의가 필요합니다.
구체적인 내용은 좀 더 아래쪽에 있는 Licensing_ 항목의 내용을 참고하세요.

만약에 개발환경을 구축하고자 하는 경우에는 아래처럼 |poetry|_ 를 활용해 구성합니다.

.. code-block:: console

    $ # Install poetry using pipx
    $ python -m pip install pipx
    $ python -m pipx ensurepath
    $ pipx install poetry

    $ # Clone repository
    $ git clone https://github.com/elbakramer/koapy.git
    $ cd koapy/

    $ # Install dependencies and hooks
    $ poetry install
    $ poetry run pre-commit install

이외에 자세한 설치방법과 관련해서는 Installation_ 문서를 참고하세요.

.. _PyPI: https://pypi.org/project/koapy/
.. _backtrader: https://github.com/mementum/backtrader
.. |koapy.backtrader| replace:: ``koapy.backtrader``
.. _`koapy.backtrader`: https://github.com/elbakramer/koapy/tree/master/koapy/backtrader
.. |poetry| replace:: ``poetry``
.. _`poetry`: https://python-poetry.org/
.. _Installation: https://koapy.readthedocs.io/en/latest/installation.html


Usage
-----

설치 이후 일반적인 사용법에 대해서는 Usage_ 를 참고하세요.

추가적으로 사용법과 관련된 다양한 예시들은 examples_ 폴더 및 notebooks_ipynb_ 폴더에서도 확인 가능합니다.
혹시나 notebooks_ipynb_ 폴더의 ``.ipynb`` 파일들을 Github 을 통해서 보는데 문제가 있는 경우,
해당 노트북 주소를 nbviewer_ 에 입력하여 확인해보세요.

현재 알파 단계이기 때문에 많은 기능들이 실제로 문제없이 동작하는지 충분히 테스트되지 않았습니다.
만약에 실전 트레이딩에 사용하려는 경우 자체적으로 충분한 테스트를 거친 후 사용하시기 바랍니다.
개발자는 라이브러리 사용으로 인해 발생하는 손실에 대해 어떠한 책임도 지지 않습니다.

또한 알파 단계에서 개발이 진행되면서 라이브러리의 구조가 계속 급격하게 변경될 수 있으니 참고 바랍니다.

.. _Usage: https://koapy.readthedocs.io/en/latest/usage.html
.. _examples: https://github.com/elbakramer/koapy/tree/master/koapy/examples
.. _notebooks_ipynb: https://github.com/elbakramer/koapy/tree/master/docs/source/notebooks_ipynb
.. _nbviewer: https://nbviewer.jupyter.org/


Licensing
---------

KOAPY 는 다중 라이선스 방식으로 배포되며,
사용자는 자신의 의도 및 사용 방식에 따라 아래 라이선스 옵션들 중 하나를 선택해 사용할 수 있습니다.

* `MIT License`_
* `Apache License 2.0`_
* `GNU General Public License v3.0`_ or later

라이선스 선택과 관련하여 추천하는 가이드라인은 아래와 같습니다.

MIT License
~~~~~~~~~~~

* 일반적인 사용자에게 알맞습니다.
* 짧고 단순한 라이선스를 선호하시면 해당 라이선스를 선택하세요.

Apache License 2.0
~~~~~~~~~~~~~~~~~~

* MIT 라이선스와 큰 차이는 없지만, 특허와 관련해서 명시적인 허가조항이 있습니다.
* 추후 특허권 침해 소송이 우려되는 경우 MIT 라이선스 대신에 선택하시면 됩니다.

GNU General Public License v3.0 or later
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* FSF_/GPL_ 이 추구하는 Copyleft_ 의 가치를 따르신다면 선택 가능한 옵션중 하나입니다.
* 이외에 backtrader_ 관련 기능들을 활용하시는 경우, KOAPY 는 **반드시** GPLv3+ 로만 배포되어야 합니다.
* 구체적으로 아래와 같은 경우들에 하나라도 포함된다면 GPLv3+ 배포 조건에 해당됩니다.

  * 설치시 ``pip install koapy[backtrader]`` 명령으로 설치
  * 사용시 |koapy.backtrader|_ 모듈 하위의 기능들을 사용

* 이것은 backtrader_ 가 GPLv3+ 로 배포되고 있으며,
  해당 라이선스의 요구사항에 따라 그것을 사용하는 소프트웨어 또한 GPLv3+ 로 배포되어야 하기 때문입니다.

각 라이선스의 허가 및 요구사항과 관련해서 쉽게 정리된 내용은 `tl;drLegal`_ 에서 참고하실 수 있습니다.

다만 위의 내용이 법률적 조언은 아닌 점 참고 바랍니다.

.. _`MIT License`: https://spdx.org/licenses/MIT.html
.. _`Apache License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`GNU General Public License v3.0`: https://www.gnu.org/licenses/gpl-3.0.html

.. _FSF: https://www.fsf.org/
.. _GPL: https://www.gnu.org/licenses/licenses.html#GPL
.. _Copyleft: https://www.gnu.org/licenses/copyleft.html

.. _`tl;drLegal`: https://tldrlegal.com/

.. |koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget| replace:: ``koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget``
.. _`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget`: https://github.com/elbakramer/koapy/blob/master/koapy/backend/kiwoom_open_api_plus/core/KiwoomOpenApiPlusQAxWidget.py
.. |koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication| replace:: ``koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication``
.. _`koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication`: https://github.com/elbakramer/koapy/blob/master/koapy/backend/kiwoom_open_api_plus/pyside2/KiwoomOpenApiPlusManagerApplication.py


Reference
---------

개발과정에 있어서 참고하거나 전체적인 투자과정에서 같이 보면 좋을 것 같아 보이는 자료들을 모아봤습니다.

* `파이썬으로 배우는 알고리즘 트레이딩`_
* `퀀트투자를 위한 키움증권 API (파이썬 버전)`_
* `시스템 트레이딩`_
* `systrader79의 왕초보를 위한 주식투자`_

.. _`파이썬으로 배우는 알고리즘 트레이딩`: https://wikidocs.net/book/110
.. _`퀀트투자를 위한 키움증권 API (파이썬 버전)`: https://wikidocs.net/book/1173
.. _`시스템 트레이딩`: https://igotit.tistory.com/840
.. _`systrader79의 왕초보를 위한 주식투자`: https://stock79.tistory.com/


Credits
-------

This package was created with Cookiecutter_ and the `elbakramer/cookiecutter-poetry`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elbakramer/cookiecutter-poetry`: https://github.com/elbakramer/cookiecutter-poetry
