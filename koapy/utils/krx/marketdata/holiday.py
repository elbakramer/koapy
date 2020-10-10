import re
import datetime
import logging

import requests

from koapy.config import config

user_agent = config.get('koapy.utils.krx.user_agent')

oldest_year_available = 1975

def download_holidays_as_dict(year=None, page_first_call=False):
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
        'search_bas_yy': str(year if year is not None else now.year),
        'gridTp': 'KRX',
        'pagePath': '/contents/MKD/01/0110/01100305/MKD01100305.jsp',
        'code': code,
    }
    if page_first_call:
        data['pageFirstCall'] = 'Y'
    response = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', headers=headers, data=data)
    body = response.json()
    return body

def download_entire_holidays_as_dicts():
    now = datetime.datetime.now()
    current_year = now.year
    results = []
    years = range(current_year, oldest_year_available - 1, -1)
    num_years = len(years)
    for i, year in enumerate(years):
        logging.debug('Downloading holidays for year %d (%d/%d)', year, i + 1, num_years)
        page_first_call = i == 0
        result = download_holidays_as_dict(year, page_first_call=page_first_call)
        results.append(result)
    # block1 = list(itertools.chain.from_iterable(map(operator.itemgetter('block1'), results)))
    # result = {'block1': block1}
    return results

def download_holidays_as_excel(f=None, year=None):
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
            'search_bas_yy': str(year if year is not None else now.year),
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
