import datetime
import logging

from koapy import KiwoomOpenApiPlusEntrypoint
from exchange_calendars import get_calendar

krx_calendar = get_calendar('XKRX')

with KiwoomOpenApiPlusEntrypoint() as context:
    # 로그인 처리
    context.EnsureConnected()

    # 종목코드
    code = '005930'

    # 가장 최근 날짜
    start_date = datetime.datetime.now()

    # 날짜 값은 datetime.datetime 타입도 되고 문자열도 됨
    # 문자열 포맷은 구체적으로, 일봉위로는 YYYYMMDD 포맷, 분봉아래로는 YYYYMMDDhhmmss 포맷 지원

    # 가장 오래된 날짜 (거래소 개장일 기준 30일 전)
    end_date = start_date - 30 * krx_calendar.day

    # 참고로 end_date 은 주어진 시간보다 큰 (같지 않은) 레코드만 가져오도록 구현되어있기 때문에 설정에 주의
    # 일반적으로 해당 날짜는 결과에서 제외되는 효과 있음, 구체적인 구간은 [start_date, end_date)

    # 위와 같은 (end_date = start_date - 30 * krx_calendar.day) 코드는 거래소가 열리는 날짜 기준 30일 전 날짜 계산하는데 사용
    # 이렇게 설정해서 일봉데이터 가져올 경우 당일 포함되면 30일치, 당일 제외되면 29일치 가져오게 됨
    # 참고로 exchange_calendars 는 현재 년도의 말일까지 미리 계산된 휴일정보를 사용하므로 미래시간은 계산이 안됨

    # 만약에 미래 시간에 대한 연산 또한 필요하다면 아래처럼 내부 구현체를 대체재로 사용해 볼 수 잇음
    #   from koapy.utils.krx.calendar.KrxHolidayCalendar import KrxBusinessDay
    #   end_date = start_date + KrxBusinessDay(30) # (거래소 개장일 기준 30일 이후)
    # 하지만 계산시 일반적인 휴일들을 제외한 임시공휴일, 선거일등은 별도 추가 데이터가 없는 한 반영되지 않으니 주의

    # 일봉 데이터
    logging.info('Requesting daily data from %s to %s', end_date, start_date)
    data = context.GetDailyStockDataAsDataFrame(code, start_date, end_date)
    print(data)

    # 15분봉 데이터
    # 분봉과 틱봉은 TR 에서 기준날짜 (기간설정시 최근날짜) 지정이 안되므로
    # 가장 최근부터 가져오고 클라이언트에서 따로 추가로 거르는 식으로 구현되어 있음
    end_date = start_date - 1 * krx_calendar.day
    logging.info('Requesting minute data from %s to %s', end_date, start_date)
    data = context.GetMinuteStockDataAsDataFrame(code, 15, start_date, end_date)
    print(data)

    # 주봉 데이터
    # 참고로 주봉은 각 주의 첫 개장일을 기준일으로 함
    end_date = start_date - 30 * krx_calendar.day
    logging.info('Requesting weekly data from %s to %s', end_date, start_date)
    data = context.GetWeeklyStockDataAsDataFrame(code, start_date, end_date)
    print(data)

    # 월봉 데이터
    # 참고로 월봉은 각 달의 첫 개장일을 기준일으로 함
    end_date = start_date - 180 * krx_calendar.day
    logging.info('Requesting monthly data from %s to %s', end_date, start_date)
    data = context.GetMonthlyStockDataAsDataFrame(code, start_date, end_date)
    print(data)

    # 30틱 데이터
    # 분봉과 틱봉은 TR 에서 기준날짜 (기간설정시 최근날짜) 지정이 안되므로
    # 가장 최근부터 가져오고 클라이언트에서 따로 추가로 거르는 식으로 구현되어 있음
    end_date = start_date - 1 * krx_calendar.day
    logging.info('Requesting tick data from %s to %s', end_date, start_date)
    data = context.GetTickStockDataAsDataFrame(code, 30, start_date, end_date)
    print(data)
