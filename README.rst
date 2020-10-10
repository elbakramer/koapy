=====
KOAPY
=====


.. image:: https://img.shields.io/pypi/v/koapy.svg
        :target: https://pypi.python.org/pypi/koapy

.. image:: https://img.shields.io/travis/elbakramer/koapy.svg
        :target: https://travis-ci.org/elbakramer/koapy

.. image:: https://readthedocs.org/projects/koapy/badge/?version=latest
        :target: https://koapy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/koapy.svg
        :target: https://pypi.python.org/pypi/koapy/
        :alt: Python versions

.. image:: https://pyup.io/repos/github/elbakramer/koapy/shield.svg
        :target: https://pyup.io/repos/github/elbakramer/koapy/
        :alt: Updates



Kiwoom Open Api Python


* Free software: MIT license
* Documentation: https://koapy.readthedocs.io.


Features
--------

KOAPY 는 `키움증권의 OpenAPI`_ 를 Python 에서 쉽게 사용할 수 있도록 만든 라이브러리 패키지 및 툴입니다.

키움에서 제공하는 OpenAPI 를 활용하는데 필요한 아래와 같은 지식들을 알지 못해도,
기본적인 Python 에 대한 지식만 어느 정도 있다면 쉽게 사용할 수 있도록 하는 것에 초점을 두었습니다.

* 키움에서 제공하는 OpenAPI 의 OCX 라이브러리 구조
* OCX 를 Python 에서 구동하기 위한 PyQt5_ 와 |QAxWidget|_ 생성
* 컨트롤에서 함수 호출을 위한 |dynamicCall|_ 함수 사용
* 이벤트 처리를 위해 적절한 |signal|_/|slot|_ 설정 및 처리

KOAPY 는 아래와 같은 기능을 제공합니다.

* PyQt5_ 를 기반한 GUI 환경에 얽매일 필요 없이 일반적인 라이브러리처럼 가져다 활용할 수 있습니다.
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

..  .. literalinclude:: ../koapy/examples/main_scenario.py
            :language: python

.. code-block:: python

    import logging
    import threading

    import grpc

    from koapy import KiwoomOpenApiContext
    from koapy import RealType

    from pprint import PrettyPrinter
    from google.protobuf.json_format import MessageToDict
    from pandas import Timestamp
    from trading_calendars import get_calendar

    pp = PrettyPrinter()
    krx_calendar = get_calendar('XKRX')

    # 주문 테스트 전에 실제로 주문이 가능한지 확인 용도
    def is_currently_in_session():
        is_in_session = False
        now = Timestamp.now()
        today_session = now.normalize()
        if krx_calendar.is_session(today_session):
            opening, closing = krx_calendar.open_and_close_for_session(today_session)
            is_in_session = opening <= now <= closing
        return is_in_session

    with KiwoomOpenApiContext() as context:
        # 로그인 예시
        logging.info('Logging in...')
        context.EnsureConnected()
        logging.info('Logged in.')

        # 기본 함수 호출 예시
        logging.info('Getting stock codes and names...')
        codes = context.GetCodeListByMarketAsList('0')
        names = [context.GetMasterCodeName(code) for code in codes]

        # 위에서 가져온 정보로 삼성전자의 code 확인
        codes_by_name = dict(zip(names, codes))
        logging.info('Checking stock code of Samsung...')
        samsung_code = codes_by_name['삼성전자']
        code = samsung_code
        logging.info('Code: %s', code)

        # TR 예시 (opt10081)
        logging.info('Getting daily stock data of Samsung...')
        data = context.GetDailyStockDataAsDataFrame(code)
        logging.info('Daily stock data:')
        print(data)

        # 조건검색 예시
        condition_name = '대형 저평가 우량주'
        logging.info('Getting stock codes with condition: %s', condition_name)
        codes, info = context.GetCodeListByCondition(condition_name, with_info=True)
        print(codes)
        print(info)

        # 주문처리 예시
        first_account_no = context.GetFirstAvailableAccount()

        request_name = '삼성전자 1주 시장가 신규 매수' # 사용자 구분명, 구분가능한 임의의 문자열
        screen_no = '0001'                           # 화면번호
        account_no = first_account_no                # 계좌번호 10자리, 여기서는 계좌번호 목록에서 첫번째로 발견한 계좌번호로 매수처리
        order_type = 1         # 주문유형, 1 : 신규매수
        code = samsung_code    # 종목코드, 앞의 삼성전자 종목코드
        quantity = 1           # 주문수량, 1주 매수
        price = 0              # 주문가격, 시장가 매수는 가격설정 의미없음
        quote_type = '03'      # 거래구분, 03 : 시장가
        original_order_no = '' # 원주문번호, 주문 정정/취소 등에서 사용

        # 현재는 기본적으로 주문수량이 모두 소진되기 전까지 이벤트를 듣도록 되어있음 (단순 호출 예시)
        if is_currently_in_session():
            logging.info('Sending order to buy %s, quantity of 1 stock, at market price...', code)
            for event in context.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no):
                pp.pprint(MessageToDict(event))
        else:
            logging.info('Cannot send an order while market is not open, skipping...')

        # 실시간 예시
        code_list = [code]
        fid_list = RealType.get_fids_by_realtype('주식시세')
        real_type = '0' # 기존 화면에 추가가 아니라 신규 생성

        # 현재는 기본적으로 실시간 이벤트를 무한정 가져옴 (커넥션 컨트롤 가능한 예시)
        logging.info('Starting to get realtime stock data for code: %s', code)
        event_iterator = context.GetRealDataForCodesAsStream(code_list, fid_list, real_type, screen_no=None, infer_fids=True, readable_names=True, fast_parse=False)

        def stop_listening():
            logging.info('Stopping to listen events...')
            event_iterator.cancel()

        threading.Timer(10.0, stop_listening).start() # 10초 이후에 gRPC 커넥션 종료하도록 설정

        # 이벤트 불러와서 출력처리
        try:
            for event in event_iterator:
                pp.pprint(MessageToDict(event))
        except grpc.RpcError as e:
            print(e)

        logging.info('End of example')


이외에 사용법과 관련한 다양한 예시들은 examples_ 폴더에서 확인 가능합니다.

해당 라이브러리는 PyPI_ 를 통해서 설치 가능합니다:

.. code-block:: console

    $ pip install koapy

..  자세한 설치방법과 관련해서는 :doc:`./installation` 을 참고하세요.
    이후 사용법에 대해서는 :doc:`./usage` 를 참고하세요.

자세한 설치방법과 관련해서는 Installation_ 을 참고하세요.

이후 사용법에 대해서는 Usage_ 를 참고하세요.

현재 알파 단계이기 때문에 많은 기능들이 실제로 문제없이 동작하는지 충분히 테스트되지 않았습니다.
만약에 실전 트레이딩에 사용하려는 경우 자체적으로 충분한 테스트를 거친 후 사용하시기 바랍니다.
개발자는 라이브러리 사용으로 인해 발생하는 손실에 대해 어떠한 책임도 지지 않습니다.

또한 알파 단계에서 개발이 진행되면서 라이브러리의 구조가 계속 급격하게 변경될 수 있으니 참고 바랍니다.

.. _`키움증권의 OpenAPI`: https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000

.. _PyQt5: https://pypi.org/project/PyQt5/
.. _매뉴얼: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf
.. _KOAStudio: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf#page=7
.. _gRPC: https://grpc.io/
.. _examples: https://github.com/elbakramer/koapy/tree/master/koapy/examples
.. _PyPI: https://pypi.org/project/koapy/
.. _Installation: https://koapy.readthedocs.io/en/latest/installation.html
.. _Usage: https://koapy.readthedocs.io/en/latest/usage.html

.. |QAxWidget| replace:: ``QAxWidget``
.. _QAxWidget: https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qaxcontainer/qaxwidget.html
.. |dynamicCall| replace:: ``dynamicCall``
.. _dynamicCall: https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qaxcontainer/qaxbase.html?highlight=dynamicCall#dynamicCall
.. |signal| replace:: ``signal``
.. _signal: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html?highlight=signal
.. |slot| replace:: ``slot``
.. _slot: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html?highlight=slot
.. |pandas.DataFrame| replace:: ``pandas.DataFrame``
.. _`pandas.DataFrame`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html

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

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
