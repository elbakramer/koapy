# check following urls
# - http://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp
# - http://global.krx.co.kr/contents/GLB/05/0501/0501110000/GLB0501110000.jsp

import re
import datetime
import requests

from koapy.utils.logging.Logging import Logging

logger = Logging.get_logger('koapy.utils.krx.marketdata.holiday')

oldest_year_available = 1975

def download_holidays_as_dict(year=None, page_first_call=False):
    now = datetime.datetime.now()
    def generate_otp():
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'global.krx.co.kr',
            'Referer': 'http://global.krx.co.kr/contents/GLB/05/0501/0501110000/GLB0501110000.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'bld': 'GLB/05/0501/0501110000/glb0501110000_01',
            'name': 'form',
            '_': str(int(now.timestamp() * 1000)),
        }
        response = requests.get('http://global.krx.co.kr/contents/COM/GenerateOTP.jspx', headers=headers, params=params)
        code = response.content
        return code
    code = generate_otp()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'global.krx.co.kr',
        'Origin': 'http://global.krx.co.kr',
        'Referer': 'http://global.krx.co.kr/contents/GLB/05/0501/0501110000/GLB0501110000.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'search_bas_yy': str(year if year is not None else now.year),
        'gridTp': 'KRX',
        'pagePath': '/contents/GLB/05/0501/0501110000/GLB0501110000.jsp',
        'code': code,
    }
    if page_first_call:
        data['pageFirstCall'] = 'Y'
    response = requests.post('http://global.krx.co.kr/contents/GLB/99/GLB99000001.jspx', headers=headers, data=data)
    body = response.json()
    return body

def download_entire_holidays_as_dicts():
    now = datetime.datetime.now()
    current_year = now.year
    results = []
    years = range(current_year, oldest_year_available - 1, -1)
    num_years = len(years)
    for i, year in enumerate(years):
        logger.debug('Downloading holidays for year %d (%d/%d)', year, i + 1, num_years)
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
            'Host': 'global.krx.co.kr',
            'Referer': 'http://global.krx.co.kr/contents/GLB/05/0501/0501110000/GLB0501110000.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'GLB/05/0501/0501110000/glb0501110000_01',
            'search_bas_yy': str(year if year is not None else now.year),
            'gridTp': 'KRX',
            'pagePath': '/contents/GLB/05/0501/0501110000/GLB0501110000.jsp',
        }
        response = requests.get('http://global.krx.co.kr/contents/COM/GenerateOTP.jspx', headers=headers, params=params)
        code = response.content
        return code
    code = generate_otp()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8,fr;q=0.7,ja;q=0.6,zh-CN;q=0.5,zh;q=0.4',
        'Cache-Control': 'max-age=0',
        'Host': 'file.krx.co.kr',
        'Origin': 'http://global.krx.co.kr',
        'Referer': 'http://global.krx.co.kr/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
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
