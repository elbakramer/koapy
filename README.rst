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

.. .. literalinclude:: ../koapy/examples/main_scenario.py
    :language: python

.. code-block:: python

    from koapy import KiwoomOpenApiContext
    from koapy import RealType

    from pprint import PrettyPrinter
    from google.protobuf.json_format import MessageToDict

    with KiwoomOpenApiContext() as context:
        # 로그인 예시
        print('Logging in...')
        context.EnsureConnected()
        print('Logged in.')

        # 함수 호출 예시
        print('Getting stock codes and names...')
        codes = context.GetCodeListByMarketAsList('0')
        names = [context.GetMasterCodeName(code) for code in codes]

        codes_by_name = dict(zip(names, codes))
        print('Checking stock code of Samsung...')
        code = codes_by_name['삼성전자']
        print('Code: %s' % code)

        # TR 예시 (opt10081)
        print('Getting daily stock data of Samsung...')
        data = context.GetDailyStockDataAsDataFrame(code)
        print('Daily stock data:')
        print(data)

        # 실시간 예시
        code_list = [code]
        fid_list = RealType.get_fids_by_realtype('주식시세')
        real_type = '0'

        pp = PrettyPrinter()

        print('Starting to get realtime stock data for code: %s' % code)
        for event in context.WatchRealDataForCodesAsStream(code_list, fid_list, real_type, screen_no=None, infer_fids=True, readable_names=True, fast_parse=False):
            pp.pprint(MessageToDict(event))

이외에 사용법과 관련한 다양한 예시들은 examples_ 폴더에서 확인 가능합니다.

해당 라이브러리는 PyPI_ 를 통해서 설치 가능합니다:

.. code-block:: console

    $ pip install koapy

.. 자세한 설치방법과 관련해서는 :doc:`./installation` 을 참고하세요.

.. 이후 사용법에 대해서는 :doc:`./usage` 를 참고하세요.

자세한 설치방법과 관련해서는 Installation_ 을 참고하세요.

이후 사용법에 대해서는 Usage_ 를 참고하세요.

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


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
