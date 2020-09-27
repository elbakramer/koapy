import re
import datetime
import requests

from koapy.config import config

from koapy.utils.krx.holiday.KrxBusinessDay import KrxBusinessDay

def get_last_krx_datetime():
    """
    대학수학능력 시험일에 한시간씩 늦춰지는건 고려하지 않음
    """
    today = datetime.datetime.now()
    last = today + KrxBusinessDay(0)
    if last == today:
        last_end = datetime.datetime.combine(last.date(), datetime.time(15, 30))
        if last > last_end:
            last = last_end
    elif last > today:
        last = today - KrxBusinessDay(1)
        last_end = datetime.datetime.combine(last.date(), datetime.time(15, 30))
        last = last_end
    return last

user_agent = config.get('koapy.utils.krx.user_agent')

def get_holidays_as_dict():
    now = datetime.datetime.now()
    def generate_otp():
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'marketdata.krx.co.kr',
            'Referer': 'http://marketdata.krx.co.kr/mdi',
            'User-Agent': user_agent,
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'bld': 'MKD/01/0110/01100305/mkd01100305_01',
            'name': 'form',
            '_': str(int(now.timestamp() * 1000)),
        }
        response = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx', headers=headers, params=params)
        code = response.content
        return code
    code = generate_otp()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'marketdata.krx.co.kr',
        'Origin': 'http://marketdata.krx.co.kr',
        'Referer': 'http://marketdata.krx.co.kr/mdi',
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'search_bas_yy': str(now.year),
        'gridTp': 'KRX',
        'pagePath': '/contents/MKD/01/0110/01100305/MKD01100305.jsp',
        'code': code,
        'pageFirstCall': 'Y',
    }
    response = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', headers=headers, data=data)
    body = response.json()
    return body

def download_holidays_as_excel(f=None):
    now = datetime.datetime.now()
    def generate_otp():
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'marketdata.krx.co.kr',
            'Referer': 'http://marketdata.krx.co.kr/mdi',
            'User-Agent': user_agent,
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/01/0110/01100305/mkd01100305_01',
            'search_bas_yy': str(now.year),
            'gridTp': 'KRX',
            'pagePath': '/contents/MKD/01/0110/01100305/MKD01100305.jsp',
        }
        response = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx', headers=headers, params=params)
        code = response.content
        return code
    code = generate_otp()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Host': 'file.krx.co.kr',
        'Origin': 'http://marketdata.krx.co.kr',
        'Referer': 'http://marketdata.krx.co.kr/mdi',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
    }
    data = {
        'code': code,
    }
    response = requests.post('http://file.krx.co.kr/download.jspx', headers=headers, data=data)
    if f is not None:
        if hasattr(f, 'write'):
            f.write(response.content)
        elif isinstance(f, str):
            filename = f
            with open(filename, 'wb') as f:
                f.write(response.content)
    else:
        filename = re.findall("filename=(.+)", response.headers['Content-Disposition'])[0]
        with open(filename, 'wb') as f:
            f.write(response.content)
    return response

if __name__ == '__main__':
    print(get_last_krx_datetime())
