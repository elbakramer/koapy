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


Introduction
------------

KOAPY 는 `키움증권의 OpenAPI+`_ 를 Python_ 에서 쉽게 사용할 수 있도록 만든
라이브러리 패키지 및 툴입니다.

키움에서 제공하는 OpenAPI+ 를 활용하는데 필요한 구체적인 지식들을 전혀 알지 못해도,
기본적인 Python_ 에 대한 지식만 어느 정도 있다면 쉽게 사용할 수 있도록 하는 것에
초점을 두었습니다.

예를 들어 Python_ 기준으로 아래와 같은 내용들을 잘 모르더라도 충분히 모든 기능을
사용할 수 있음을 의미합니다.

* 키움에서 제공하는 OpenAPI+ 의 OCX 라이브러리 구조
* OCX 를 Python_ 에서 구동하기 위해 PyQt5_/PySide2_ 라이브러리의 |QAxWidget|_ 생성
* 컨트롤에서 함수 호출을 위해 |dynamicCall|_ 함수 사용
* 이벤트 처리를 위해 적절한 |signal|_/|slot|_ 설정 및 이벤트 처리

.. _`키움증권의 OpenAPI+`: https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000
.. _Python: https://www.python.org/

.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt/
.. _PySide2: https://doc.qt.io/qtforpython/index.html

.. |QAxWidget| replace:: ``QAxWidget``
.. _QAxWidget: https://doc.qt.io/qt-5/qaxwidget.html
.. |dynamicCall| replace:: ``dynamicCall``
.. _dynamicCall: https://doc.qt.io/qt-5/qaxbase.html#dynamicCall
.. |signal| replace:: ``signal``
.. _signal: https://doc.qt.io/qt-5/signalsandslots.html#signals
.. |slot| replace:: ``slot``
.. _slot: https://doc.qt.io/qt-5/signalsandslots.html#slots


Showcase
--------

테이블 데이터 처리를 위한 pandas 임포트
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> import pandas as pd

엔트리포인트 객체 생성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from koapy import KiwoomOpenApiPlusEntrypoint

.. code-block:: python

    >>> entrypoint = KiwoomOpenApiPlusEntrypoint()

키움증권 서버와의 연결 확인 및 로그인 처리
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> entrypoint.IsConnected()
    False
    >>> entrypoint.EnsureConnected()
    True
    >>> entrypoint.IsConnected()
    True

종목 리스트 및 종목 코드와 이름 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> code_list = entrypoint.GetCodeListByMarKetAsList("0")
    >>> code_list
    ['000020', '000040', '000050', '000060', '000070', ...]

.. code-block:: python

    >>> name_list = [entrypoint.GetMasterCodeName(code) for code in code_list]
    >>> name_list
    ['동화약품', 'KR모터스', '경방', '메리츠화재', '삼양홀딩스', ...]

.. code-block:: python

    >>> code_by_name = {name: code for code, name in zip(code_list, name_list)}

.. code-block:: python

    >>> name = "삼성전자"
    >>> code = code_by_name[name]
    >>> code
    '005930'

단일 종목의 기본정보 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> info = entrypoint.GetStockBasicInfoAsDict(code)
    >>> info
    {'종목코드': '005930', '종목명': '삼성전자', '결산월': '12', '액면가': '100', '자본금': '7780', '상장주식': '5969783', '신용비율': '+0.12', '연중최고': '+79800', '연중최저': '-71200', '시가총액': '4417639', '시가총액비중': '', '외인소진률': '+52.09', '대용가': '57170', 'PER': '19.27', 'EPS': '3841', 'ROE': '10.0', 'PBR': '1.88', 'EV': '5.09', 'BPS': '39406', '매출액': '2368070', '영업이익': '359939', '당기순이익': '264078', '250최고': '+86400', '250최저': '-68300', '시가': '+74300', '고가': '+74600', '저가': '+73400', '상한가': '+95200', '하한가': '-51400', '기준가': '73300', '예상체결가': '-0', '예상체결수량': '0', '250최고가일': '20210202', '250최고가대비율': '-14.35', '250최저가일': '20211013', '250최저가대비율': '+8.35', '현재가': '+74000', '대비기호': '2', '전일대비': '+700', '등락율': '+0.95', '거래량': '12730034', '거래대비': '-71.74', '액면가단위': '원', '유통주식': '4459119', '유통비율': '74.7'}

복수 종목의 기본정보 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> code_list_info = entrypoint.GetStockQuoteInfoAsDataFrame(code_list)
    >>> code_list_info
            종목코드                      종목명     현재가    기준가   전일대비 전일대비기호    등락율  \
    0     000020                     동화약품  +12450  12300   +150      2  +1.22
    1     000040                    KR모터스    +810    790    +20      2  +2.53
    2     000050                       경방  +14450  14200   +250      2  +1.76
    3     000060                    메리츠화재   49450  49450      0      3   0.00
    4     000070                    삼양홀딩스  +90700  88400  +2300      2  +2.60
    ...      ...                      ...     ...    ...    ...    ...    ...
    1744  580031  KB 인버스 KOSDAQ150 선물 ETN  -10930  10960    -30      5  -0.27
    1745  580032     KB 레버리지 구리 선물 ETN(H)  -20515  20560    -45      5  -0.22
    1746  580033   KB 인버스 2X 구리 선물 ETN(H)  +18350  18280    +70      2  +0.38
    1747  580010         KB Wise 분할매매 ETN  +10820  10770    +50      2  +0.46
    1748  590018       미래에셋 중국 심천 100 ETN  +18810  18645   +165      2  +0.88

            거래량   거래대금   체결량  ...    ELW만기일 미결제약정 미결제전일대비 이론가 내재변동성 델타 감마 쎄타 베가  \
    0     135513   1670  +500  ...  00000000
    1     230165    186   -10  ...  00000000
    2       6214     89    97  ...  00000000
    3     411584  20423    -4  ...  00000000
    4       9052    813    +5  ...  00000000
    ...      ...    ...   ...  ...       ...   ...     ...  ..   ... .. .. .. ..
    1744       2      0    -1  ...  00000000
    1745       0      0        ...  00000000
    1746      17      0   +10  ...  00000000
    1747       0      0        ...  00000000
    1748       1      0    +1  ...  00000000

        로
    0
    1
    2
    3
    4
    ...  ..
    1744
    1745
    1746
    1747
    1748

    [1749 rows x 63 columns]

특정 종목의 차트 데이터 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> chart_data = entrypoint.GetDailyStockDataAsDataFrame(code)
    >>> chart_data
            종목코드    현재가       거래량     거래대금        일자     시가     고가     저가 수정주가구분  \
    0     005930  74000  12730034   941413  20220204  74300  74600  73400
    1             73300  17744721  1314506  20220203  74900  74900  73300
    2             73300  21367447  1552586  20220128  71300  73700  71200
    3             71300  22274777  1603685  20220127  73800  74000  71300
    4             73300  12976730   955547  20220126  73900  74400  73100
    ...      ...    ...       ...      ...       ...    ...    ...    ...    ...
    9797           8010      4970        1  19850109   8240   8240   7950
    9798           8300     12930        4  19850108   8400   8400   8300
    9799           8410     11810        3  19850107   8400   8500   8390
    9800           8390      1660        0  19850105   8400   8440   8390
    9801           8450      1710        0  19850104   8500   8500   8450

        수정비율 대업종구분 소업종구분 종목정보 수정주가이벤트 전일종가
    0
    1
    2
    3
    4
    ...   ...   ...   ...  ...     ...  ...
    9797
    9798
    9799
    9800
    9801

    [9802 rows x 15 columns]

키움증권의 TR 메타 정보 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from koapy import KiwoomOpenApiPlusTrInfo

.. code-block:: python

    >>> tr_info_list = KiwoomOpenApiPlusTrInfo.get_trinfo_list()

.. code-block:: python

    >>> data = pd.DataFrame.from_records([(info.tr_code, info.name) for info in tr_info_list], columns=['tr_code', 'name'])
    >>> data
          tr_code             name
    0    opt10001         주식기본정보요청
    1    opt10059      종목별투자자기관별요청
    2    opt10087         시간외단일가요청
    3    opt50037       코스피200지수요청
    4    opt90005       프로그램매매추이요청
    ..        ...              ...
    220  opw20013  계좌미결제청산가능수량조회요청
    221  opw20014     선옵실시간증거금산출요청
    222  opw20015    옵션매도주문증거금현황요청
    223  opw20016      신용융자 가능종목요청
    224  opw20017        신용융자 가능문의

    [225 rows x 2 columns]

OPT10001 TR 요청 전송 및 응답 처리 (싱글데이터)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> opt10001_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code("opt10001")
    >>> opt10001_info
    KiwoomOpenApiPlusTrInfo('opt10001', '주식기본정보요청', 'STOCK', '', '1', '', [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 6, 9001)], '주식기본정보', [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 389), KiwoomOpenApiPlusTrInfo.Field('종목명', 20, 50, 302), KiwoomOpenApiPlusTrInfo.Field('결산월', 40, 20, 315), KiwoomOpenApiPlusTrInfo.Field('액면가', 60, 20, 310), KiwoomOpenApiPlusTrInfo.Field('자본금', 80, 20, 309), KiwoomOpenApiPlusTrInfo.Field('상장주식', 100, 20, 312), KiwoomOpenApiPlusTrInfo.Field('신용비율', 120, 20, 329), KiwoomOpenApiPlusTrInfo.Field('연중최고', 140, 20, 1006), KiwoomOpenApiPlusTrInfo.Field('연중최저', 160, 20, 1009), KiwoomOpenApiPlusTrInfo.Field('시가총액', 180, 20, 311), KiwoomOpenApiPlusTrInfo.Field('시가총액비중', 200, 20, 336), KiwoomOpenApiPlusTrInfo.Field('외인소진률', 220, 20, 314), KiwoomOpenApiPlusTrInfo.Field('대용가', 240, 20, 308), KiwoomOpenApiPlusTrInfo.Field('PER', 260, 20, 1600), KiwoomOpenApiPlusTrInfo.Field('EPS', 280, 20, 1604), KiwoomOpenApiPlusTrInfo.Field('ROE', 300, 20, 1630), KiwoomOpenApiPlusTrInfo.Field('PBR', 320, 20, 1601), KiwoomOpenApiPlusTrInfo.Field('EV', 340, 20, 1608), KiwoomOpenApiPlusTrInfo.Field('BPS', 360, 20, 1605), KiwoomOpenApiPlusTrInfo.Field('매출액', 380, 20, 1610), KiwoomOpenApiPlusTrInfo.Field('영업이익', 400, 20, 1611), KiwoomOpenApiPlusTrInfo.Field('당기순이익', 420, 20, 1614), KiwoomOpenApiPlusTrInfo.Field('250최고', 440, 20, 1000), KiwoomOpenApiPlusTrInfo.Field('250최저', 460, 20, 1003), KiwoomOpenApiPlusTrInfo.Field('시가', 480, 20, 16), KiwoomOpenApiPlusTrInfo.Field('고가', 500, 20, 17), KiwoomOpenApiPlusTrInfo.Field('저가', 520, 20, 18), KiwoomOpenApiPlusTrInfo.Field('상한가', 540, 20, 305), KiwoomOpenApiPlusTrInfo.Field('하한가', 560, 20, 306), KiwoomOpenApiPlusTrInfo.Field('기준가', 580, 20, 307), KiwoomOpenApiPlusTrInfo.Field('예상체결가', 600, 20, 10023), KiwoomOpenApiPlusTrInfo.Field('예상체결수량', 620, 20, 10024), KiwoomOpenApiPlusTrInfo.Field('250최고가일', 640, 20, 1001), KiwoomOpenApiPlusTrInfo.Field('250최고가대비율', 660, 20, 1002), KiwoomOpenApiPlusTrInfo.Field('250최저가일', 680, 20, 1004), KiwoomOpenApiPlusTrInfo.Field('250최저가대비율', 700, 20, 1005), KiwoomOpenApiPlusTrInfo.Field('현재가', 720, 20, 10), KiwoomOpenApiPlusTrInfo.Field('대비기호', 740, 20, 25), KiwoomOpenApiPlusTrInfo.Field('전일대비', 760, 20, 11), KiwoomOpenApiPlusTrInfo.Field('등락율', 780, 20, 12), KiwoomOpenApiPlusTrInfo.Field('거래량', 800, 20, 13), KiwoomOpenApiPlusTrInfo.Field('거래대비', 820, 20, 30), KiwoomOpenApiPlusTrInfo.Field('액면가단위', 840, 20, 796), KiwoomOpenApiPlusTrInfo.Field('유통주식', 840, 20, 1683), KiwoomOpenApiPlusTrInfo.Field('유통비율', 840, 20, 1684)], '', [])

    >>> opt10001_info.inputs
    [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 6, 9001)]

    >>> opt10001_info.single_outputs
    [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 389), KiwoomOpenApiPlusTrInfo.Field('종목명', 20, 50, 302), KiwoomOpenApiPlusTrInfo.Field('결산월', 40, 20, 315), KiwoomOpenApiPlusTrInfo.Field('액면가', 60, 20, 310), KiwoomOpenApiPlusTrInfo.Field('자본금', 80, 20, 309), KiwoomOpenApiPlusTrInfo.Field('상장주식', 100, 20, 312), KiwoomOpenApiPlusTrInfo.Field('신용비율', 120, 20, 329), KiwoomOpenApiPlusTrInfo.Field('연중최고', 140, 20, 1006), KiwoomOpenApiPlusTrInfo.Field('연중최저', 160, 20, 1009), KiwoomOpenApiPlusTrInfo.Field('시가총액', 180, 20, 311), KiwoomOpenApiPlusTrInfo.Field('시가총액비중', 200, 20, 336), KiwoomOpenApiPlusTrInfo.Field('외인소진률', 220, 20, 314), KiwoomOpenApiPlusTrInfo.Field('대용가', 240, 20, 308), KiwoomOpenApiPlusTrInfo.Field('PER', 260, 20, 1600), KiwoomOpenApiPlusTrInfo.Field('EPS', 280, 20, 1604), KiwoomOpenApiPlusTrInfo.Field('ROE', 300, 20, 1630), KiwoomOpenApiPlusTrInfo.Field('PBR', 320, 20, 1601), KiwoomOpenApiPlusTrInfo.Field('EV', 340, 20, 1608), KiwoomOpenApiPlusTrInfo.Field('BPS', 360, 20, 1605), KiwoomOpenApiPlusTrInfo.Field('매출액', 380, 20, 1610), KiwoomOpenApiPlusTrInfo.Field('영업이익', 400, 20, 1611), KiwoomOpenApiPlusTrInfo.Field('당기순이익', 420, 20, 1614), KiwoomOpenApiPlusTrInfo.Field('250최고', 440, 20, 1000), KiwoomOpenApiPlusTrInfo.Field('250최저', 460, 20, 1003), KiwoomOpenApiPlusTrInfo.Field('시가', 480, 20, 16), KiwoomOpenApiPlusTrInfo.Field('고가', 500, 20, 17), KiwoomOpenApiPlusTrInfo.Field('저가', 520, 20, 18), KiwoomOpenApiPlusTrInfo.Field('상한가', 540, 20, 305), KiwoomOpenApiPlusTrInfo.Field('하한가', 560, 20, 306), KiwoomOpenApiPlusTrInfo.Field('기준가', 580, 20, 307), KiwoomOpenApiPlusTrInfo.Field('예상체결가', 600, 20, 10023), KiwoomOpenApiPlusTrInfo.Field('예상체결수량', 620, 20, 10024), KiwoomOpenApiPlusTrInfo.Field('250최고가일', 640, 20, 1001), KiwoomOpenApiPlusTrInfo.Field('250최고가대비율', 660, 20, 1002), KiwoomOpenApiPlusTrInfo.Field('250최저가일', 680, 20, 1004), KiwoomOpenApiPlusTrInfo.Field('250최저가대비율', 700, 20, 1005), KiwoomOpenApiPlusTrInfo.Field('현재가', 720, 20, 10), KiwoomOpenApiPlusTrInfo.Field('대비기호', 740, 20, 25), KiwoomOpenApiPlusTrInfo.Field('전일대비', 760, 20, 11), KiwoomOpenApiPlusTrInfo.Field('등락율', 780, 20, 12), KiwoomOpenApiPlusTrInfo.Field('거래량', 800, 20, 13), KiwoomOpenApiPlusTrInfo.Field('거래대비', 820, 20, 30), KiwoomOpenApiPlusTrInfo.Field('액면가단위', 840, 20, 796), KiwoomOpenApiPlusTrInfo.Field('유통주식', 840, 20, 1683), KiwoomOpenApiPlusTrInfo.Field('유통비율', 840, 20, 1684)]

    >>> opt10001_info.multi_outputs
    []

.. code-block:: python

    >>> request_name = "주식기본정보요청"  # 사용자 구분명, 구분가능한 임의의 문자열
    >>> tr_code = "opt10001"
    >>> screen_no = "0001"  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    >>> inputs = {
    ...    "종목코드": "005930",  # 삼성전자 종목코드
    ... }

    >>> output = {}

    >>> for event in entrypoint.TransactionCall(request_name, tr_code, screen_no, inputs):
    ...     names = event.single_data.names
    ...     values = event.single_data.values
    ...     for name, value in zip(names, values):
    ...         output[name] = value

    >>> output
    {'종목코드': '005930', '종목명': '삼성전자', '결산월': '12', '액면가': '100', '자본금': '7780', '상장주식': '5969783', '신용비율': '+0.12', '연중최고': '+79800', '연중최저': '-71200', '시가총액': '4417639', '시가총액비중': '', '외인소진률': '+52.09', '대용가': '57170', 'PER': '19.27', 'EPS': '3841', 'ROE': '10.0', 'PBR': '1.88', 'EV': '5.09', 'BPS': '39406', '매출액': '2368070', '영업이익': '359939', '당기순이익': '264078', '250최고': '+86400', '250최저': '-68300', '시가': '+74300', '고가': '+74600', '저가': '+73400', '상한가': '+95200', '하한가': '-51400', '기준가': '73300', '예상체결가': '-0', '예상체결수량': '0', '250최고가일': '20210202', '250최고가대비율': '-14.35', '250최저가일': '20211013', '250최저가대비율': '+8.35', '현재가': '+74000', '대비기호': '2', '전일대비': '+700', '등락율': '+0.95', '거래량': '12730034', '거래대비': '-71.74', '액면가단위': '원', '유통주식': '4459119', '유통비율': '74.7'}

OPT10081 TR 요청 전송 및 응답 처리 (멀티데이터)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> opt10081_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code("opt10081")
    >>> opt10081_info
    KiwoomOpenApiPlusTrInfo('opt10081', '주식일봉차트조회요청', 'SCHART', '', '1', '3003', [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 9001), KiwoomOpenApiPlusTrInfo.Field('기준일자', 20, 20, 9004), KiwoomOpenApiPlusTrInfo.Field('수정주가구분', 40, 20, 9055)], '주식일봉차트', [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 9001)], '주식일봉차트조회', [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 9001), KiwoomOpenApiPlusTrInfo.Field('현재가', 0, 20, 10), KiwoomOpenApiPlusTrInfo.Field('거래량', 40, 20, 13), KiwoomOpenApiPlusTrInfo.Field('거래대금', 60, 20, 14), KiwoomOpenApiPlusTrInfo.Field('일자', 80, 20, 22), KiwoomOpenApiPlusTrInfo.Field('시가', 100, 20, 16), KiwoomOpenApiPlusTrInfo.Field('고가', 120, 20, 17), KiwoomOpenApiPlusTrInfo.Field('저가', 140, 20, 18), KiwoomOpenApiPlusTrInfo.Field('수정주가구분', 160, 20, 3502), KiwoomOpenApiPlusTrInfo.Field('수정비율', 180, 20, 3503), KiwoomOpenApiPlusTrInfo.Field('대업종구분', 200, 20, 317), KiwoomOpenApiPlusTrInfo.Field('소업종구분', 220, 20, 318), KiwoomOpenApiPlusTrInfo.Field('종목정보', 240, 20, 370), KiwoomOpenApiPlusTrInfo.Field('수정주가이벤트', 260, 20, 3501), KiwoomOpenApiPlusTrInfo.Field('전일종가', 280, 20, 346)])

    >>> opt10081_info.inputs
    [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 9001), KiwoomOpenApiPlusTrInfo.Field('기준일자', 20, 20, 9004), KiwoomOpenApiPlusTrInfo.Field('수정주가구분', 40, 20, 9055)]

    >>> opt10081_info.single_outputs
    [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 9001)]

    >>> opt10081_info.multi_outputs
    [KiwoomOpenApiPlusTrInfo.Field('종목코드', 0, 20, 9001), KiwoomOpenApiPlusTrInfo.Field('현재가', 0, 20, 10), KiwoomOpenApiPlusTrInfo.Field('거래량', 40, 20, 13), KiwoomOpenApiPlusTrInfo.Field('거래대금', 60, 20, 14), KiwoomOpenApiPlusTrInfo.Field('일자', 80, 20, 22), KiwoomOpenApiPlusTrInfo.Field('시가', 100, 20, 16), KiwoomOpenApiPlusTrInfo.Field('고가', 120, 20, 17), KiwoomOpenApiPlusTrInfo.Field('저가', 140, 20, 18), KiwoomOpenApiPlusTrInfo.Field('수정주가구분', 160, 20, 3502), KiwoomOpenApiPlusTrInfo.Field('수정비율', 180, 20, 3503), KiwoomOpenApiPlusTrInfo.Field('대업종구분', 200, 20, 317), KiwoomOpenApiPlusTrInfo.Field('소업종구분', 220, 20, 318), KiwoomOpenApiPlusTrInfo.Field('종목정보', 240, 20, 370), KiwoomOpenApiPlusTrInfo.Field('수정주가이벤트', 260, 20, 3501), KiwoomOpenApiPlusTrInfo.Field('전일종가', 280, 20, 346)]

.. code-block:: python

    >>> import datetime

    >>> date = datetime.datetime.now().strftime("%Y%m%d")
    >>> date
    '20220206'

.. code-block:: python

    >>> request_name = "주식일봉차트조회요청"  # 사용자 구분명, 구분가능한 임의의 문자열
    >>> tr_code = "opt10081"
    >>> screen_no = "0001"  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    >>> inputs = {
    ...     "종목코드": "005930",  # 삼성전자 종목코드
    ...     "기준일자": "20220206",  # 가장 최근 날짜의 YYYYMMDD 포맷
    ...     "수정주가구분": "0",  # 0:일반주가, 1:수정주가
    ... }

    >>> data_list = []

    >>> for event in entrypoint.TransactionCall(request_name, tr_code, screen_no, inputs):
    ...     columns = event.multi_data.names
    ...     records = [values.values for values in event.multi_data.values]
    ...     data = pd.DataFrame.from_records(records, columns=columns)
    ...     data_list.append(data)

    >>> data = pd.concat(data_list, axis=0).reset_index(drop=True)
    >>> data
            종목코드    현재가       거래량     거래대금        일자     시가     고가     저가 수정주가구분  \
    0     005930  74000  12730034   941413  20220204  74300  74600  73400
    1             73300  17744721  1314506  20220203  74900  74900  73300
    2             73300  21367447  1552586  20220128  71300  73700  71200
    3             71300  22274777  1603685  20220127  73800  74000  71300
    4             73300  12976730   955547  20220126  73900  74400  73100
    ...      ...    ...       ...      ...       ...    ...    ...    ...    ...
    9797           8010      4970        1  19850109   8240   8240   7950
    9798           8300     12930        4  19850108   8400   8400   8300
    9799           8410     11810        3  19850107   8400   8500   8390
    9800           8390      1660        0  19850105   8400   8440   8390
    9801           8450      1710        0  19850104   8500   8500   8450

        수정비율 대업종구분 소업종구분 종목정보 수정주가이벤트 전일종가
    0
    1
    2
    3
    4
    ...   ...   ...   ...  ...     ...  ...
    9797
    9798
    9799
    9800
    9801

    [9802 rows x 15 columns]

조건검색 조건식 설정 불러오기
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> entrypoint.IsConditionLoaded()
    False
    >>> entrypoint.EnsureConditionLoaded()
    1
    >>> entrypoint.IsConditionLoaded()
    True

불러온 조건식 목록 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> condition_name_list = entrypoint.GetConditionNameListAsList()
    >>> condition_name_list
    [(0, '대형 저평가 우량주'), (1, '중소형 저평가주')]

조건식 단순 검색
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> condition_name = "대형 저평가 우량주"
    >>> condition_met_code_list, condition_met_code_list_info = entrypoint.GetCodeListByCondition(condition_name, with_info=True)

    >>> condition_met_code_list
    ['000240', '001800', '001880', '003230', '003550', '004000', '006040', '006390', '006650', '007700', '009970', '011780', '014830', '020000', '021240', '025540', '030520', '033290', '033780', '036830', '042420', '056190', '057050', '060150', '064960', '069080', '081660', '095660', '096530', '110790', '111770', '137310', '161390', '161890', '185750', '192080', '192400', '200130', '243070', '271560', '284740', '285130', '294870', '300720', '950130']

    >>> condition_met_code_list_info  # same as entrypoint.GetStockQuoteInfoAsDataFrame(condition_met_code_list)
          종목코드        종목명      현재가     기준가   전일대비 전일대비기호     등락율      거래량    거래대금  \
    0   000240     한국앤컴퍼니   +13500   13400   +100      2   +0.75    56484     760
    1   001800     오리온홀딩스   +14600   14250   +350      2   +2.46    69827    1008
    2   001880       DL건설   -27950   28050   -100      5   -0.36    20925     583
    3   003230       삼양식품   +91300   90000  +1300      2   +1.44    58660    5289
    4   003550         LG   +76300   74600  +1700      2   +2.28   249415   18925
    ..     ...        ...      ...     ...    ...    ...     ...      ...     ...
    40  284740      쿠쿠홈시스   +36700   35900   +800      2   +2.23    30134    1102
    41  285130      SK케미칼  +130500  129500  +1000      2   +0.77    58032    7544
    42  294870  HDC현대산업개발   +15600   14600  +1000      2   +6.85  3145356   49106
    43  300720      한일시멘트   +19250   18750   +500      2   +2.67   159419    3021
    44  950130     엑세스바이오   -18400   22400  -4000      5  -17.86  5877689  119649

        체결량  ...    ELW만기일 미결제약정 미결제전일대비 이론가 내재변동성 델타 감마 쎄타 베가 로
    0   5549  ...  00000000
    1     +1  ...  00000000
    2    369  ...  00000000
    3     +2  ...  00000000
    4   +100  ...  00000000
    ..   ...  ...       ...   ...     ...  ..   ... .. .. .. .. ..
    40    -3  ...  00000000
    41    -1  ...  00000000
    42   -25  ...  00000000
    43    -4  ...  00000000
    44   -36  ...  00000000

    [45 rows x 63 columns]

GRPC 스트림 처리 관련 유틸리티 함수 (데모 목적)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> import contextlib
    >>> import threading
    >>> import warnings

    >>> import grpc

    >>> @contextlib.contextmanager
    ... def warn_on_rpc_error_context():
    ...     try:
    ...         yield
    ...     except grpc.RpcError as e:
    ...         warnings.warn(str(e))

    >>> def warn_on_rpc_error(stream):
    ...     with warn_on_rpc_error_context():
    ...         for event in stream:
    ...             yield event

    >>> def cancel_after(stream, after):
    ...     timer = threading.Timer(after, stream.cancel)
    ...     timer.start()
    ...     return warn_on_rpc_error(stream)

조건식 실시간 검색
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> condition_name = "중소형 저평가주"
    >>> stream = entrypoint.GetCodeListByConditionAsStream(condition_name)

    >>> condition_met_code_list = []
    >>> data_list = []

    >>> for event in cancel_after(stream, 10):
    ...     if event.name == "OnReceiveTrCondition":
    ...         initially_included_code_list = event.arguments[1].string_value
    ...         initially_included_code_list = initially_included_code_list.rstrip(';').split(';') if initially_included_code_list else []
    ...         condition_met_code_list.extend(initially_included_code_list)
    ...     elif event.name == "OnReceiveRealCondition":
    ...         code = event.arguments[0].string_value
    ...         condition_type = event.arguments[1].string_value
    ...         if condition_type == "I":
    ...             code_inserted = code
    ...             condition_met_code_list.append(code_inserted)
    ...         elif condition_type == "D":
    ...             code_deleted = code
    ...             condition_met_code_list.remove(code_deleted)
    ...     elif event.name == "OnReceiveTrData":
    ...         columns = event.multi_data.names
    ...         records = [values.values for values in event.multi_data.values]
    ...         data = pd.DataFrame.from_records(records, columns=columns)
    ...         data_list.append(data)

    >>> condition_met_code_list
    ['900290', '900310', '900340', '002170', '017890', '023600', '036190', '037710', '049430', '073560', '140910', '187870', '192440', '210540', '225220', '263690', '352700', '950190', '900280', '900250']

    >>> data_list
    []

계좌정보 확인
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> account_list = entrypoint.GetAccountList()
    >>> account_list
    ['8014526011']

    >>> first_account_no = entrypoint.GetFirstAvailableAccount()
    >>> first_account_no
    '8014526011'

주문 요청 (삼성전자 시장가 매수)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> request_name = "삼성전자 1주 시장가 신규 매수"  # 사용자 구분명, 구분가능한 임의의 문자열
    >>> screen_no = "0001"  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    >>> account_no = "8014526011"  # 계좌번호 10자리, 여기서는 계좌번호 목록에서 첫번째로 발견한 계좌번호로 매수처리
    >>> order_type = 1  # 주문유형, 1:신규매수
    >>> code = "005930"  # 종목코드, 앞의 삼성전자 종목코드
    >>> quantity = 1  # 주문수량, 1주 매수
    >>> price = 0  # 주문가격, 시장가 매수는 가격 설정 의미 없으므로 기본값 0 으로 설정
    >>> quote_type = "03"  # 거래구분, 03:시장가
    >>> original_order_no = ""  # 원주문번호, 주문 정정/취소 등에서 사용

    >>> stream = entrypoint.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no)

    >>> for event in warn_on_rpc_error(stream):
    ...     if event.name == "OnReceiveTrData":
    ...         order_no = event.single_data.values[0]
    ...     elif event.name == "OnReceiveChejanData":
    ...         gubun = event.arguments[0].string_value
    ...         data = dict(event.single_data.names, event.single_data.values)
    ...         if gubun == "0":
    ...             status = data["주문상태"]
    ...             if status == "접수":
    ...                 pass
    ...             elif status == "체결":
    ...                 orders_filled = data["체결량"]
    ...                 orders_left = data["미체결수량"]
    ...             elif status == "확인":
    ...                 org_order_no = data["원주문번호"]
    ...                 assert original_order_no == org_order_no
    ...         elif gubun in ["1", "4"]:
    ...             stocks = data["보유수량"]

키움증권의 실시간 데이터 메타 정보 확인
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from koapy import KiwoomOpenApiPlusRealType

.. code-block:: python

    >>> realtype_list = KiwoomOpenApiPlusRealType.get_realtype_info_list()

.. code-block:: python

    >>> realtype_descs = [realtype.desc for realtype in realtype_list]
    >>> realtype_descs
    ['주식시세', '주식체결', '주식상하한', '주식우선호가', '주식호가잔량', '주식시간외호가', '주식당일거래원', 'ETF NAV', 'ELW 지표', 'ELW 이론가', '주식예상체결', '주식종목정보', '임의연장정보', 'ECN주식시세', 'ECN주식체결', 'ECN주식우선호가', 'ECN주식호가잔량', 'ECN주식시간외호가', 'ECN주식당일거래원', '시간외종목정보', '주식거래원', '주식거래원(1LINE)', '종목별프로그램매매', 'VI정적예상가', 'VI발동/해제-종목별', '종목별프로그램매매2', '종목투자자(잠정)', '종목투자자(거래소)', '대주가능수량', '선물옵션우선호가', '선물시세', '선물호가잔량', '선물이론가', '선물기초자산시세', '실시간상하한가', '옵션시세', '옵션호가잔량', '옵션이론가', '주식옵션시세', '주식옵션호가잔량', '주식옵션이론가', '업종지수', '업종등락', '자체업종지수', '예상업종지수', '시황/뉴스', '환률', '장시작시간', '투자자ticker', '상하한가폭변경', 'VI발동/해제', '투자자별매매', '프로그램매매', '해외시세', '주문체결', '파생잔고', '현물잔고', '예수금', '해외주문체결', '해외잔고', '순간체결량', '주문체결서버상태', '증거금', 'CFD주문', 'CFD체결', 'CFD마진콜경고', 'CFD입출고', '자유포멧', '조건검색', '일반신호', '리얼잔고', '해외리얼잔고', '리얼잔고총합', '해외잔고총합', '스톱로스', '선물옵션합계', '스톱주문', 'CFD주문체결', 'CFD리얼잔고', 'CFD리얼잔고총합', '모니터링 실시간LOG', '주식선물호가잔량', '실시간증거금', 'X-Ray순간체결량', '매입인도체결', '매입인도호가', '코넥스경매매체결', '데이터셋실시간', '홍콩체결', '홍콩시세', '홍콩호가잔량', '홍콩단일가시세', '홍콩업종지수', '홍콩실시간상하한가', '수동자동주문', '자동주문결과', 'TS고저변경', '잔고편입', '기준가변경', '멀티차단', '잔고청산삭제', '후강퉁체결', '후강퉁시세', '후강퉁호가잔량', '후강퉁단일가시세', '후강퉁업종지수', '미체결통보시스템', '채널K실시간티커', '빅데이터종목1분', '빅데이터종목10분', '빅데이터종목1시간', '빅데이터종목당일', '빅데이터뉴스', '신호관리자투자정보', '빅데이터급상승', '빅데이터종목30초', '알-종목포착이탈', '알-매도감시시작', '알-매도감시포착', '알-주문결과', '알-청산시작', '알-청산완료', '알-감시시작', '알-내조건식수정', '알-주문조건수정', '알-제한여부', '알-멀티차단', '알-TS변경', '알-모의주문체결', '알-모의현물잔고', '알-모의 주문체결', '알-모의 리얼잔고', '알-모의리얼잔고총합', '채권체결', '채권호가잔량', '소액채권체결', '소액채권호가잔량', 'CME시세', 'CME미결제약정', 'CME호가잔량', 'EUF시세', 'EUF호가잔량', 'EUREX시세', 'EUREX호가', '배치데이터갱신', '종목마스터갱신', '해외주식주문', '해외주식체결', '해외실시간잔고조회', '미국입출고', '미국종목변경', 'CME/EUREX주문', 'CME/EUREX체결', 'CME배치', 'EUREX배치', 'CME미체결', 'CME실시간잔고', 'CME잔고합', '분할반복주문']

    >>> realtype_info = KiwoomOpenApiPlusRealType.get_realtype_info_by_name("주식시세")
    >>> realtype_info
    KiwoomOpenApiPlusRealType('0A', '주식시세', 21, [10, 11, 12, 27, 28, 13, 14, 16, 17, 18, 25, 26, 29, 30, 31, 32, 311, 822, 567, 568, 732])

    >>> fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name("주식시세")
    >>> fid_list
    [10, 11, 12, 27, 28, 13, 14, 16, 17, 18, 25, 26, 29, 30, 31, 32, 311, 822, 567, 568, 732]

    >>> KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(10)
    '현재가'

    >>> fid_names = KiwoomOpenApiPlusRealType.get_field_names_by_realtype_name("주식시세")
    >>> fid_names
    ['현재가', '전일대비', '등락율', '매도호가', '매수호가', '누적거래량', '누적거래대금', '시가', '고가', '저가', '전일대비기호', '거래량전일대비', '거래대금증감', '전일거래량대비율', '거래회전율', '거래비용', '시가총액', '822', '567', '568', '732']

실시간 데이터 요청 (삼성전자 주식시세 실시간 데이터 요청)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> code_list = ["005930"]
    >>> fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name("주식시세")
    >>> opt_type = "0"  # 기존 화면에 추가가 아니라 신규 생성

    >>> stream = entrypoint.GetRealDataForCodesAsStream(
    ...     code_list,
    ...     fid_list,
    ...     opt_type,
    ...     screen_no=None,  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    ...     infer_fids=True,  # True 로 설정 시 주어진 fid_list 를 고집하지 말고 이벤트 처리 함수의 인자로 전달받는 실시간데이터 이름에 따라 유연하게 fid_list 를 추론
    ...     readable_names=True,  # True 로 설정 시 각 fid 마다 숫자 대신 읽을 수 있는 이름으로 변환하여 반환
    ...     fast_parse=False,  # True 로 설정 시 이벤트 처리 함수내에서 데이터 값 읽기 시 GetCommRealData() 함수 호출 대신, 이벤트 처리 함수의 인자로 넘어오는 데이터를 직접 활용, infer_fids 가 True 로 설정된 경우만 유의미함
    ... )

    >>> for event in cancel_after(stream, 10):
    ...     if event.name == "OnReceiveRealData":
    ...         data = dict(event.single_data.names, event.single_data.values)
    ...         if "현재가" in data:
    ...             current_price = data["현재가"]

사용 종료 후 엔트리포인트 객체 리소스 해제 (연결 해제 및 서버 어플리케이션 종료)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

직접 ``close()`` 메소드 호출:

.. code-block:: python

    >>> entrypoint.close()

혹은 처음부터 컨텍스트 매니저 형태로 리소스 관리:

.. code-block:: python

    >>> with KiwoomOpenApiPlusEntrypoint() as entrypoint:
    ...     entrypoint.EnsureConnected()
    ...     ...


Installation
------------

대표적으로 아래와 같이 PyPI_ 를 통해서 설치가 가능합니다:

.. code-block:: console

    $ pip install koapy

만약에 개발 환경을 구축하고자 하는 경우에는 |poetry|_ 를 활용해 구성합니다.

.. code-block:: console

    $ # Install poetry (here using pipx)
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
.. |poetry| replace:: ``poetry``
.. _poetry: https://python-poetry.org/
.. _Installation: https://koapy.readthedocs.io/en/latest/installation.html


Features
--------

KOAPY 는 아래와 같은 방향성을 가지고 개발되었습니다.

GUI 어플리케이션만으로 제한되지 않는 다양한 사용성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

일반적으로 인터넷 등지에서 접하기 쉬운 관련 예시들을 처음으로 따라가다 보면, 자기도
모르는 사이에 Qt 기반 어플리케이션을 하나 만들고, 버튼을 하나 추가하고, 이후 모든
기능들을 죄다 해당 버튼을 클릭 시 작동하는 콜백 함수 하나에 쑤셔 넣고 있는.. 자신을
발견하게 되더군요.

.. code-block:: python

    # https://wikidocs.net/4240

    import sys

    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QAxContainer import *

    class MyWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("PyStock")
            self.setGeometry(300, 300, 300, 150)

            self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

            btn1 = QPushButton("Login", self)
            btn1.move(20, 20)
            btn1.clicked.connect(self.btn1_clicked)

            btn2 = QPushButton("Check state", self)
            btn2.move(20, 70)
            btn2.clicked.connect(self.btn2_clicked)

        def btn1_clicked(self):
            ret = self.kiwoom.dynamicCall("CommConnect()")

        def btn2_clicked(self):
            if self.kiwoom.dynamicCall("GetConnectState()") == 0:
                self.statusBar().showMessage("Not connected")
            else:
                self.statusBar().showMessage("Connected")

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        myWindow = MyWindow()
        myWindow.show()
        app.exec_()

사실 기반 라이브러리가 애초에 OCX 형태로서 제공되는 것도 있고, 다른 여러 가지 이유들로
인해 이처럼 GUI 어플리케이션 형태로 개발을 하는 것이 자연스러운 흐름이고 절대
잘못되었다고 생각되진 않습니다.

다만 이러한 GUI 환경이 일반적으로 Python 에서 REPL 혹은 Jupyter Notebook 등을 통해서
인터랙티브하게 결과 값들을 확인해가면서 조금씩 개발해 나가던 것과는 거리가 멀어지면서
결론적으로 생산성이 떨어지게 되는 건 아닌가 하는 생각이 들었고, 그로 인해 KOAPY 의
기본적인 인터페이스는 기반이 되는 Qt 환경을 개발자가 직접적으로 고려하진 않으면서도
기능은 쉽게 사용해 볼 수 있게 끔 하는 게 좋겠다고 생각했습니다.

따라서 KOAPY 의 기본적인 디자인은 우선 외적으로 봤을 때 이게 내부적으로는 Qt 같은
환경하에서 돌아간다는 것을 바로 알아챌 순 없게 끔 되어 있습니다. 그리고 기본적인
기능들을 이용하는 데에 있어서도 버튼 클릭 등의 이벤트에 기반한 호출보단 일반적인 함수
호출과 같은 명령형 프로그래밍이 가능하도록 디자인 하였으며, 문서에서도 해당 사용
시나리오들을 중점적으로 먼저 소개하고 있습니다.

.. code-block:: python

    from koapy import KiwoomOpenApiPlusEntrypoint

    with KiwoomOpenApiPlusEntrypoint() as entrypoint:
        entrypoint.EnsureConnected()
        is_connected = entrypoint.IsConnected()
        print(is_connected)


결론적으로 PyQt5_ 혹은 PySide2_ 를 기반한 GUI 환경에 얽매일 필요 없이 일반적인
라이브러리처럼 가져다 활용할 수 있으며, 여전히 GUI 기반 어플리케이션 개발이 필요하다면
내부적으로 사용되는 요소들을 통해 직접 GUI 방향으로 개발을 할 수도 있습니다.

.. code-block:: python

    from koapy.compat.pyside2.QtWidgets import QApplication, QMainWindow
    from koapy import KiwoomOpenApiPlusQAxWidget

    class MyWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.kiwoom = KiwoomOpenApiPlusQAxWidget()
            ...


함수 호출등의 과정에서 일반적인 Python 의 관습을 크게 해치지 않는 매끄러운 인터페이스 구성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Qt 를 통해서 COM/OLE/OCX 객체의 메서드를 호출하려면 |dynamicCall|_ 함수를 활용해야 합니다.

해당 |dynamicCall|_ 함수는 호출하고자 하는 메서드의 프로토타입을 문자열 형태 인자로서
입력하도록 되어있는데, 단순하게는 매번 메서드를 호출하고자 할 때마다 해당 메서드의
프로토타입이 어떻게 생겼는지를 문서 등을 참고하고 일일이 적어 넣어줘야 할 수 있습니다.

.. code-block:: python

    control = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    control.dynamicCall("SetInputValue(const QString&, const QString&)", "종목코드", code)

그 다음으로 보다 나은 방식으로는 이러한 프로토타입을 모든 함수들에 대해서 확인해서
간단한 래퍼 함수들을 만들어두고 활용하는 게 있겠죠.

.. code-block:: python

    def SetInputValue(name, value):
        return control.dynamicCall("SetInputValue(const QString&, const QString&)", name, value)

일반적으로는 이런 방식들로도 충분히 사용하는데 무리가 없으리라 생각됩니다만
개인적으로는 위와 같은 접근 방식에서 몇 가지 우려되는 점들이 신경이 쓰였습니다.

* 프로토타입을 입력하거나 래퍼 함수들을 만들어 넣는 과정에서 발생할 수 있는 휴먼에러
* 래퍼 함수들을 만들어 놓았더라도 추후 함수의 목록 혹은 특정 함수의 프로토타입에서
  변경이 발생하는 경우 매번 직접적인 대응이 필요함

따라서 KOAPY 에서는 이러한 지원 함수 목록 및 함수별 프로토타입 정보 확인, 그리고
이것들을 활용해 특정 메서드를 호출하는 과정까지를 어떻게 프로그래밍적으로 대응할 수
없을까를 고민했고, 현재는 OpenAPI+ OCX 의 TypeLib 정보를 읽어와 메서드들을 동적으로
생성하도록 구현해 위에서 우려했던 점들을 해결했습니다.

최종적으론 컨트롤 함수 호출 시 매뉴얼의 명세에 적혀있는 형태 그대로 Python 함수였던
것처럼 호출이 가능하며, 이후는 KOAPY 가 유연하게 처리합니다. 매번 명세에 맞게
|dynamicCall|_ 함수의 인자를 적어 넣거나, 모든 존재하는 함수에 대해 미리 래퍼 함수를
손 아프게 만들어놓을 필요가 없습니다.

.. code-block:: python

    control = KiwoomOpenApiPlusQAxWidget()
    control.SetInputValue("종목코드", code)

이벤트 처리 및 비동기 프로그래밍 관련 복잡하지 않은 인터페이스 제공
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

비동기 프로그래밍은 일반적으로 어렵습니다. 특히 OpenAPI+ 및 KOAPY 의 경우를 예로
들어보면 아래와 같은 고민해 볼 만한 부분들이 있습니다.

* 여러 요청에 대한 응답 결과들을 이벤트 타입별 하나씩의 통로로 처리하기 때문에 그들
  간의 교통정리부터 필요합니다.
* 콜백 함수 내에서 OpenAPI+ 가 기대하는 혹은 가이드하는 방식에 맞춰서 처리해 주어야
  하는 특정 단계 혹은 프로세스가 존재하며 이를 적절히 대응해 주어야 합니다.
* 콜백 함수에서 받은 결과를 최종적으로 해당 결과가 필요한 곳으로 (일반적으론 요청한
  대상에게로) 잘 전달해 주어야 합니다.

KOAPY 에서는 위의 문제들을 나름의 방식대로 고민하였고 문제들을 해결하여 더 쉽고 나은
인터페이스를 사용자에게 제공하고 있습니다.

구체적으로 예를 하나 들자면, 일반적인 요청-응답 과정에서 내부적으로 gRPC
클라이언트-서버 관계를 만들어 요청자가 gRPC 를 통해 특정 요청을 전달하면, 이후 gRPC
서버에서는 해당 요청에 대한 응답들만 추려서 결과를 요청자측에 스트림 형태로 전달하도록
디자인되어 있는데요. 여기서 교통정리 및 결과 전달 문제가 자연스럽게 해결되며 부수적으로
사용자 입장에서는 직접 콜백 함수를 다루기보다는 간접적으로 스트림을
(``for`` 문을 활용하여) 다룸으로써 더 쉽게 비동기 프로그래밍이 필요한 기능들을 사용할
수 있는 이점이 있습니다.

PySide2 를 통한 직접적인 방식:

.. code-block:: python

    # 컨트롤 객체
    control = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    # 이벤트 시그널
    on_receive_tr_data_signal = SIGNAL("OnReceiveTrData(const QString&, const QString&, const QString&, const QString&, const QString&, int, const QString&, const QString&, const QString&)")

    # 이벤트 콜백 함수
    def on_receive_tr_data(screen_no, request_name, tr_code, record_name, prev_next, data_length, error_code, message, splmmsg):
        handle_event(...)

        # 이벤트 처리 후 필요하다면 등록된 콜백 함수 제거
        if should_disconnect:
            control.disconnect(on_receive_tr_data_signal, on_receive_tr_data)

    # 이벤트 시그널에 콜백 함수 연결
    control.connect(on_receive_tr_data_signal, on_receive_tr_data)

    # TR 입력값 설정
    control.dynamicCall("SetInputValue(const QString&, const QString&)", ..., ...)
    ...

    # TR 요청
    err_code = control.dynamicCall(
        "CommRqData(const QString&, const QString&, int, const QString&)",
        request_name,
        tr_code,
        prev_next,
        screen_no,
    )

KOAPY 방식:

.. code-block:: python

    # TR 요청 후 이벤트가 스트림 형태로 반환
    for event in entrypoint.TransactionCall(request_name, tr_code, screen_no, inputs):
        handle_event(event)

결론적으로는 사용자가 이벤트 처리 및 비동기 프로그래밍에 익숙하지 않더라도 그보다
비교적 쉬운 인터페이스를 통해 관련 기능들을 활용할 수 있습니다.

더 나아가서는 가장 간단한 로그인 처리부터 TR/실시간 데이터 처리, 그리고 주문처리까지
다양한 시나리오에 대한 기본 이벤트 처리 로직을 구현해 제공해 사용자들이 비동기
프로그래밍이 필요한 기능 중 주로 사용되는 기능들에 쉽게 접근할 수 있도록 했습니다.

.. code-block:: python

    stream = entrypoint.LoginCall()
    stream = entrypoint.TransactionCall(request_name, tr_code, screen_no, inputs)
    stream = entrypoint.RealCall(screen_no, codes, fids, opt_type)
    stream = entrypoint.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no)

여러 일반적인 시나리오들에 대한 다양한 기본 구현체들을 제공
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KOAPY 에서는 일반적으로 자주 사용되는 기능들에 대해서 사용자들이 쉽게 접근할 수 있도록,
예를 들어 주식 기본정보 요청부터 일봉/분봉 등 시세 데이터 확인 그리고 예수금/잔고 확인 등등에 대해 미리 구현된 함수를 제공합니다.

.. code-block:: python

    stock_info = entrypoint.GetStockBasicInfoAsDict(stock_code)
    stock_chart_data = entrypoint.GetDailyStockDataAsDataFrame(stock_code)

    account_deposit = entrypoint.GetDepositInfo(account_no)
    account_evaluation = (
        account_evaluation_summary,
        account_evaluation_per_stock,
    ) = entrypoint.GetAccountEvaluationStatusAsSeriesAndDataFrame(account_no)

이 중에 함수 호출 결과 중 테이블성 정보들은 |pandas.DataFrame|_ 타입으로 제공해 이후 분석 및 처리가 유용하게끔 했습니다.

.. |pandas.DataFrame| replace:: ``pandas.DataFrame``
.. _`pandas.DataFrame`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html

개발과정에서 라이브러리 밖을 드나들 필요가 없도록 자주 확인이 필요한 여러가지 메타 정보들을 함께 제공
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

일반적으로 인터넷 등지에서 접하기 쉬운 관련 대부분 예시들은 사용자가 OpenAPI+ 에 대한
여러 가지 메타정보들을 이미 다 알고 있다는 걸 가정하고, 아니면 적어도 외부 참고자료를
확인하는 것을 가정하고 작성되어 있는 경우가 많습니다.

예를 들어 TR 의 입력과 출력 데이터 구조, 실시간 데이터별 FID 목록, 에러코드에 대한
설명문 등이 이러한 메타정보들에 해당되는데요. 앞서 함수 호출 방식에서의 이슈와 비슷하게,
이러한 정보들을 매번 참고 자료를 확인하고 그에 맞춰 개발하는 방식에는 어느 정도 한계가
있습니다.

따라서 KOAPY 에서는 이러한 정보들을 개발하는 과정에서 언어 내 라이브러리에서 바로 조회
및 활용이 가능하도록 포함시켜 제공합니다. 이로 인해 일차적으로 사용자 입장에서는 매번
매뉴얼_ 이나 KOAStudio_ 를 열어서 참고하고 이후 일일이 하나씩 하드코딩할 필요가
없어졌습니다.

.. code-block:: python

    from koapy import KiwoomOpenApiPlusTrInfo
    tr_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code("opt10001")

    from koapy import KiwoomOpenApiPlusRealType
    realtype_info = KiwoomOpenApiPlusRealType.get_realtype_info_by_name("주식시세")

    from koapy import KiwoomOpenApiPlusError
    error_message = KiwoomOpenApiPlusError.get_error_message_by_code(-101)

덧붙여서 TR 관련 정보나 실시간 데이터 관련 정보들은 OpenAPI+ 가 설치되어 있는 경우
해당 경로의 데이터를 참고해 동적으로 생성하도록 되어있는데요. 이로 인해 직접 하드코딩
등을 했을 때 발생할 수 있는 이슈 없이, 매번 업데이트 시 변경된 내용이 바로바로 적용될
수 있는 이점 또한 가지고 있습니다.

.. _매뉴얼: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf
.. _KOAStudio: https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.5.pdf#page=7

라이브러리 호환성으로 인해 특정 환경이 강제되는 것을 우회할 수 있도록 시스템 구성
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

키움증권의 OpenAPI+ 는 32bit 환경만 제공하고 있기 때문에 이를 사용하는 쪽도 자연스럽게
32bit 기반이 되어야 합니다.

여기서는 Python_ 을 32bit 로 사용해야 하는 조건이 붙게 되는 것인데요. 몇몇 외부
서드파티들에서는 더 이상 32bit 를 지원하지 않는 경우도 많아 다양한 서드파티 기능들과
접목시키기에는 32bit 제약이 번거로운 점이 많습니다.

KOAPY 에서는 이를 해소하기 위해 gRPC_ 서버-클라이언트 형태의 구성을 잡아 서버에서는
32bit 기반으로 OpenAPI+ 의 핵심 기능만 제공하도록 하고, 클라이언트에서는 이런 32bit
제약 없이 결과들을 받아서 이후 여러 서드파티 기능들과 함께 활용할 수 있도록 했습니다.

앞에서는 주로 32bit 제약을 가지고 이야기했지만 더 나아가서는 gRPC_ 의 많은 언어들에
대한 확장성을 활용하여 Python 이외에 gRPC_ 에서 지원하는 다른 언어들로 클라이언트를
작성해 사용하는 방식으로도 확장이 가능합니다.

또한 Python_ 에서 Qt_ 를 사용하기 위해서는 PyQt5_ 혹은 PySide2_ 를 사용해야 하는데요.
KOAPY 에서는 라이선스 등을 고려해서 기본값으로 PySide2_ 를 사용하도록 되어있지만,
사용자의 필요성에 따라 PySide2_ 대신 PyQt5_ 를 사용하려 할 때 쉽게 변경할 수 있도록
|qtpy|_ 를 통해서 지원하고 있습니다.

.. _gRPC: https://grpc.io/

.. _Python: https://www.python.org/
.. _Qt: https://www.qt.io/

.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt/
.. _PySide2: https://doc.qt.io/qtforpython/index.html

.. |qtpy| replace:: ``qtpy``
.. _qtpy: https://github.com/spyder-ide/qtpy

키움증권의 OpenAPI+ 기능 자체 이외에 부수적으로 필요할만한 다양한 기능들을 추가로 제공
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KOAPY 는 키움증권의 OpenAPI+ 핵심 기능 이외에 전체적인 개발 및 활용에 필요한 다양한
부가기능들을 추가로 제공합니다.

* TR 호출 시 호출 횟수 제한 회피
* KRX 거래소 휴장일 확인 (|exchange_calendars|_ API 활용)
* 알람 및 메시지 기능 (|discord.py|_ API 활용)

.. |exchange_calendars| replace:: ``exchange_calendars``
.. _exchange_calendars: https://github.com/gerrymanoim/exchange_calendars
.. |discord.py| replace:: ``discord.py``
.. _`discord.py`: https://discordpy.readthedocs.io/en/stable/

라이브러리 뿐만 아니라 관련 기능들을 추가적인 코드 구현없이 쉽게 사용해볼 수 있도록 (+ 개념 증명 목적으로서) CLI 제공
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

굳이 Python 코드를 작성하지 않더라도 기본적인 기능들을 활용해 볼 수 있도록 여러
커맨드를 포함하는 CLI 를 제공합니다.

CLI 를 활용하면 마켓별 코드 목록 확인, 주식 기본 정보 확인, 일봉/분봉 데이터 확인 및
저장, 실시간 데이터 구독 등 다양한 기능들을 코드 구현 없이 사용할 수 있습니다.

.. code-block:: console

    $ koapy get stockcode --market=0
    $ koapy get stockinfo --code=005930
    $ koapy get daily --code=005930 --output=005930.xlsx
    $ koapy watch --code=005930 --realtype="주식시세"

서버도 CLI 커맨드로 쉽게 띄울 수 있습니다.

.. code-block:: console

    $ koapy serve


Usage
-----

설치 이후 일반적인 사용법에 대해서는 Usage_ 를 참고하세요.

추가적으로 사용법과 관련된 다양한 예시들은 examples_ 폴더 및 notebooks_ipynb_ 폴더에서도 확인 가능합니다.
혹시나 notebooks_ipynb_ 폴더의 ``.ipynb`` 파일들을 Github 을 통해서 보는데 문제가 있는 경우,
해당 노트북 주소를 nbviewer_ 에 입력하여 확인해 보세요.

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
* 구체적으로 |koapy.backtrader|_ 모듈 하위의 기능들을 사용한다면 GPLv3+ 배포 조건에 해당됩니다.
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

.. _backtrader: https://github.com/mementum/backtrader
.. |koapy.backtrader| replace:: ``koapy.backtrader``
.. _`koapy.backtrader`: https://github.com/elbakramer/koapy/tree/master/koapy/backtrader

.. _`tl;drLegal`: https://tldrlegal.com/


Credits
-------

이 패키지는 Cookiecutter_ 와 `elbakramer/cookiecutter-poetry`_ 프로젝트 탬플릿을 사용하여 생성되었습니다.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elbakramer/cookiecutter-poetry`: https://github.com/elbakramer/cookiecutter-poetry
