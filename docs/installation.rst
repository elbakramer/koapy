.. highlight:: shell

============
Installation
============


Stable release
--------------

To install KOAPY, run this command in your terminal:

.. code-block:: console

    $ pip install koapy

This is the preferred method to install KOAPY, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for KOAPY can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/elbakramer/koapy

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/elbakramer/koapy/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/elbakramer/koapy
.. _tarball: https://github.com/elbakramer/koapy/tarball/master


Environment
-----------

KOAPY 라이브러리 설치 이전의 환경구성 부터 최종 라이브러리 설치까지의 전체과정에 대해 설명합니다.

OS
==

Windows 10 64bit 환경을 권장합니다.

비록 라이브러리가 32bit 환경을 강제하지만 그렇다고 굳이 OS 까지 32bit 를 사용할 필요는 없습니다.

Kiwoom Open Api
===============

키움증권의 계좌개설 및 HTS ID 연결까지는 진행되어있는 것을 가정합니다.

`키움 OpenAPI+`_ 페이지를 방문해서 사용절차의 Step 1 부터 Step 4 까지 순서대로 따라가시면 됩니다.
물론 Step 3 의 "OCX 탑재 프로그램 제작" 은 이후 KOAPY 를 활용해서 제작할 수 있는 부분이니
당장은 제공되는 자료들을 참고만 하는 수준이면 됩니다.

마지막 Step 4 의 상시 모의투자는 개발 과정에서 테스트 및 디버깅을 위해 필수로 신청합니다.
아니면 실제서버에 대해서 요청을 할건데, 여러분의 자산은 소중합니다.

.. _`키움 OpenAPI+`: https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408000000

Python (Anaconda)
=================

Python 을 설치하는데 여러 방법이 있겠지만, 여기서는 Anaconda distribution 을 설치하는 내용을 다룹니다.

`Anaconda Products`_ 페이지를 방문해서 하단으로 스크롤을 하면 Anaconda Installers 라고 해서 설치 파일들을 다운로드 받을 수 있도록 되어있습니다.
여기서 Windows 하단의 "64-Bit Graphical Installer" 를 다운로드 받아 설치합니다.
설치시에 그냥 바로 32-Bit Python 을 설치하는 옵션도 있지만.. 개인적으로 권장하진 않습니다.
여기서는 64-Bit Anaconda 를 먼저 설치 후 ``conda env`` 를 통해 32-Bit 가상환경을 추가로 구성합니다.

설치가 완료되었으면 시작화면의 검색창에 Anaconda 를 검색하는 경우 ``Anaconda Prompt (Anaconda3)`` 프로그램을 찾을 수 있습니다.
실행하면 검은색 프롬프트가 뜨는데, 여기서 ``python``, ``conda`` 등의 명령어를 사용할 수 있습니다.
``python`` 명령을 입력해 제대로 동작하는지 테스트 해봅시다. 이후 문제가 없으면 ``exit()`` 를 입력해 Python 인터프리터에서 빠져나옵니다.

.. code-block:: console

    $ python
    Python 3.8.3 (default, Jul  2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> exit()

혹시나 ``pyreadline`` 혹은 ``history`` 관련 경고가 출력되는 경우에 아래 명령을 통해 패치된 버전으로 교체합니다.

.. code-block:: console

    $ pip install -I git+https://github.com/elbakramer/pyreadline.git

이제 32-Bit Python 을 설치할 차례입니다.
아래 명령을 한줄씩 앞서 띄워놓은 프롬프트에 입력해 수행합니다.

.. code-block:: console

    $ set CONDA_FORCE_32BIT=1
    $ conda create -n x86 python=3.8 anaconda

여기서 ``-n`` 뒤에 오는 ``x86`` 값은 굳이 예시와 같지 않아도 됩니다.
이후에 32-Bit 환경이 필요할 때마다 환경을 불러오는 데에 키값으로 활용될 값입니다.
추후 여러 번 사용하면서 알아보기에/입력하기에 편할법한 값으로 대체하셔도 문제없습니다.

동의를 구하는 단계에서는 ``y`` 를 입력해줍니다.

.. code-block:: console

    ...
    Proceed ([y]/n)? y
    ...

설치가 완료되었으면 이제 아래 명령을 통해 32-Bit Python 환경을 불러옵니다.

.. code-block:: console

    $ conda activate x86

제대로 불러온 경우라면 입력창 앞의 괄호로 있던 ``(base)`` 가 ``(x86)`` 으로 대체될겁니다.
앞서 64-Bit 에서 테스트 했던 것과 똑같이 32-Bit 에 대해서도 문제가 없는지 확인해봅니다.

.. code-block:: console

    (x86) $ python
    Python 3.8.3 (default, Jul  2 2020, 17:28:51) [MSC v.1916 32 bit (Intel)] :: Anaconda, Inc. on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> exit()

32-Bit Python 의 설치가 완료되었습니다. ``[MSC v.1916 32 bit (Intel)]`` 구문이 출력되는 것으로 32-Bit 이 맞다는 것을 다시 한번 확인 가능합니다.
32-Bit 환경에서 다시 이전의 64-Bit ``(base)`` 환경으로 다시 돌아가고 싶은 경우에는 아래의 명령을 실행합니다.

.. code-block:: console

    (x86) $ conda deactivate

그러면 다시 앞의 ``(x86)`` 이 ``(base)`` 로 바뀌면서 64-Bit 환경으로 돌아오게 됩니다.

이제 다음부터는 ``Anaconda Prompt (Anaconda3)`` 실행 후 ``conda activate x86`` 을 통해서 32-Bit 환경을 불러오거나,
아니면 시작화면에서 ``Anaconda Prompt (x86)`` 을 찾아서 실행하면 바로 32-Bit 환경으로 시작합니다.

.. _`Anaconda Products`: https://www.anaconda.com/products/individual

KOAPY
=====

이후 KOAPY 설치는 pip_ 를 통해 설치하면 됩니다.

.. code-block:: console

    $ pip install koapy

맨 위의 :ref:`Stable release` 의 내용과 동일한 내용입니다.

OpenAPI 와의 통신을 위해서 32-Bit 환경에는 필수로 설치되어야 합니다.
OpenAPI 의 OCX 라이브러리가 32-Bit 환경만 지원하기 때문입니다.

64-Bit 환경에서의 설치는 선택사항입니다.
혹시나 64-Bit 환경에서만 지원되는 라이브러리 및 기능을 트레이딩 로직에 접목시키고자 하는 경우
32-Bit 환경에는 서버만 띄워두고, 64Bit 환경에서 gRPC 클라이언트 API 를 통해 서버에 연결해서 OpenAPI 의 모든 기능을 활용할 수 있습니다.

.. _pip: https://pip.pypa.io
