==============
Advanced Usage
==============

Getting historical data
-----------------------

아무래도 주식거래를 컴퓨터로 하는 것의 장점 중 하나는,
머신러닝 등을 통해 축적된 데이터를 기반으로 컴퓨터가 최적의 판단을 할 수 있도록 만들 수 있기 때문일 겁니다.
하지만 그러기 위해서는 맨 먼저 학습시킬 데이터부터 확보가 되어야 합니다.

KOAPY 에서는 그런 데이터 확보 프로세스를 쉽게 만들기 위해서
데이터 다운로드, 저장, 관리에 도움이 되는 여러 라이브러리를 제공합니다.

그중 하나가 :py:mod:`~.koapy.data.HistoricalStockPriceDataUpdater` 입니다.

아래는 :py:mod:`~.koapy.data.HistoricalStockPriceDataUpdater` 를 사용하는 예시입니다.

.. literalinclude:: ../koapy/examples/dump_historical_data.py
    :language: python

위의 코드가 수행하는 작업에 대해 짧게 설명하자면
``codes`` 배열에 있는 종목들에 대해서 과거 15분봉 데이터를 가져와서 ``datadir``, 즉 data 폴더 아래에 저장합니다.

위에서 설명한 주요 작업 외에도 아래와 같은 다양한 부가기능들이 들어가 있지만
이것들에 대해서 더 세부적으로 설명하진 않겠습니다.
자세한 내용은 실제로 예시 코드를 돌려보고 어떻게 동작하는지 확인하시면서 체득하거나
직접 :py:mod:`~.koapy.data.HistoricalStockPriceDataUpdater` 의 구현을 참고하시기 바랍니다.

* 가져온 데이터를 엑셀 혹은 SQLite_ 파일로 저장해 관리 가능
    * 엑셀은 데이터를 쉽게 눈으로 확인 가능하다는 이점 있음, 용량이 비교적 적음,
      매번 파일을 새로 덮어쓰는 식이기 때문에 데이터 갱신 등 관리 과정에서는 비효율적
    * SQLite_ 는 별도 툴을 통해 데이터 확인 가능, 용량은 비교적 큼, SQL 인터페이스를 통해 데이터를 효율적으로 관리 가능
* 파일이 존재하는 경우 기본으로 최근 데이터만 가져와서 병합
    * 거래소 개장 일정 기준 최신 데이터로 판단되는 경우 데이터 요청조차 하지 않음으로써 API 호출 횟수 제한 및 네트워킹 관련 효율성 증대
    * 이외에 이미 존재하는 파일은 그냥 무시하고 업데이트를 하지 않거나 반대로 아예 덮어써버리는 옵션도 있음
* 주어진 코드 목록에 포함되지 않는 데이터는 제거해서 유효한 데이터만 유지 가능
* 진행 중에 어떠한 이유로 진행이 중단된 경우 중단 시점부터 재시작 할 수 있는 기능
* 데이터 조회에 키움 OpenAPI+ 이외의 다른 백엔드 (예를 들어 대신증권 CybosPlus) 를 사용할 수 있는 옵션 제공

이 중에 다른 백엔드 사용과 관련해서 추가로 설명을 하자면,
기본적으로 :py:mod:`~.koapy.data.HistoricalStockPriceDataUpdater` 는 키움증권 OpenAPI+ 를 통해서 데이터를 조회하도록 설정이 되어있지만,
설정 파일 수정이나 객체 생성 시에 다른 인자를 설정하는 것으로 다른 증권사의 API 도 사용 가능하도록 구현이 되어 있습니다.

현재는 대신증권 CybosPlus 만 구현이 되어 있습니다. (:py:class:`~.koapy.backend.cybos.CybosPlusComObject.CybosPlusComObject`)

적어도 데이터 조회에 있어서는 대신증권 CybosPlus 가 키움증권의 OpenAPI+ 에 비해서 몇 가지 이점이 있다고 생각하는데, 그 중 일부는 아래와 같습니다.

* 데이터 조회 호출 횟수 제한량이 더 느슨한 듯 싶습니다.
    * 대신증권 CybosPlus 는 15초에 60회 호출 제한입니다.
    * 키움증권 OpenAPI+ 는 여러 제한 조건들이 다중으로 적용되는데, 장기적으로 봤을 때 1시간에 1000회 제한으로 대략 4초에 1회 꼴입니다.
* 가져올 수 있는 데이터의 기간이 더 길어서 데이터의 양도 더 많고, 더 오래된 과거 데이터를 가져올 수 있습니다.
* 데이터를 가져온 뒤에 추가적인 후처리를 거의 하지 않아도 됩니다.
  키움의 경우는 가져온 데이터에 대해서 leading zeros 를 제거한다거나
  전날대비기호가 붙어나오는 가격값들을 ``abs`` 처리한다던가 하는 부수적인 작업이 필요합니다.
* CybosPlus 를 실행해 로그인을 최초 수동으로 해놓으면 이후 매번 스크립트를 수행할 때마다 따로 로그인할 필요가 없습니다.
    * 키움 OpenAPI 를 사용하는 경우에 KOAPY 에서 제공하는 서버 같은 걸 별도로 띄우던 프로세스가 딱히 필요가 없습니다.
* 데이터 조회 API 가 동기식으로 처리가 되기 때문에 비교적 다루기가 쉽습니다.

대신증권 CybosPlus 를 사용해 볼 수 있는 방법 중 하나는 파이썬을 스크립트를 실행하는 디렉토리 (CWD/PWD) 아래
혹은 사용자 홈 폴더 아래에 다음과 같은 설정 파일을 ``koapy.conf`` 혹은 ``.koapy.conf`` 파일 이름으로 추가하는 겁니다.

.. code-block:: hocon

    {
        koapy.data.updater.default_context = "koapy.backend.cybos.CybosPlusComObject.CybosPlusComObject"
    }

설정파일 예시는 `KOAPY 의 기본 설정파일`_ 을 참고하세요.
설정파일의 포맷은 HOCON_ 포맷입니다.

CybosPlus 백엔드를 사용하기 위해선 당연하지만 CybosPlus 설치 및 실행/로그인이 되어있어야 하며,
파이썬 스크립트 수행은 32-Bit 환경에서 실행되어야 합니다.
CybosPlus 도 현재로선 32-Bit 에서만 지원하기 때문입니다.

.. _SQLite: https://www.sqlite.org/index.html
.. _`KOAPY 의 기본 설정파일`: https://github.com/elbakramer/koapy/blob/master/koapy/config.conf
.. _HOCON: https://github.com/chimpler/pyhocon
