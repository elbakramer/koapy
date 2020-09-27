import re
import requests

from koapy.config import config

user_agent = config.get('koapy.utils.krx.user_agent')

gubuns = {
    'ALL': 'ALL',
    'KOSPI': 'STK',
    'KOSDAQ': 'KSQ',
    'KONEX': 'KNX',
}

def download_stocks_as_excel(f=None, gubun=None):
    if gubun is None:
        gubun = 'ALL'
    def generate_otp():
        headers = {
            'Accept': '*/*',
            'Host': 'marketdata.krx.co.kr',
            'Referer': 'http://marketdata.krx.co.kr/mdi',
            'User-Agent': user_agent,
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'name': 'fileDown',
            'filetype': 'xls',
            'url': 'MKD/01/0110/01100305/mkd01100305_01',
            'market_gubun': gubun,
            'isu_cdnm': '전체',
            'isu_cd': '',
            'isu_nm': '',
            'isu_srt_cd': '',
            'sort_type': 'A',
            'std_ind_cd': '',
            'par_pr': '',
            'cpta_scl': '',
            'sttl_trm': '',
            'lst_stk_vl': '1',
            'in_lst_stk_vl': '',
            'in_lst_stk_vl2': '',
            'cpt': '1',
            'in_cpt': '',
            'in_cpt2': '',
            'mktpartc_no': '',
            'pagePath': '/contents/MKD/04/0406/04060100/MKD04060100.jsp',
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

def download_all_stocks_as_excel(f=None):
    return download_stocks_as_excel(f, gubuns['ALL'])

def download_kospi_stocks_as_excel(f=None):
    return download_stocks_as_excel(f, gubuns['KOSPI'])

def download_kosdaq_stocks_as_excel(f=None):
    return download_stocks_as_excel(f, gubuns['KOSDAQ'])

def download_konex_stocks_as_excel(f=None):
    return download_stocks_as_excel(f, gubuns['KONEX'])
