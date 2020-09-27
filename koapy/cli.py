"""Console script for koapy."""

import os
import locale
import logging

import click

import koapy
from koapy.utils.logging import set_verbosity

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

client_check_timeout = 3

def fail_with_usage(message=None):
    ctx = click.get_current_context()
    if message is not None:
        click.UsageError(message).show()
        click.echo()
    click.echo(ctx.get_help())
    ctx.exit(1)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(koapy.__version__, '-V', '--version')
def cli():
    pass

@cli.command(context_settings=CONTEXT_SETTINGS, short_help='Start grpc server with tray application.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, default=5, help='Verbosity.')
@click.option('--no-verbose', is_flag=True)
@click.argument('args', nargs=-1)
def serve(port, verbose, no_verbose, args):
    """
    ARGS are passed to QApplication.
    """
    app_args = []
    if port:
        app_args += ['--port', port]
    if not no_verbose and verbose > 0:
        app_args.append('-' + 'v' * verbose)
    app_args += list(args)
    from koapy.pyqt5.KiwoomOpenApiTrayApplication import KiwoomOpenApiTrayApplication
    KiwoomOpenApiTrayApplication.main(app_args)

@cli.command(context_settings=CONTEXT_SETTINGS, short_help='Ensure logged in when server is up.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def login(port, verbose):
    set_verbosity(verbose)
    from koapy import KiwoomOpenApiContext
    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout) as context:
        state = context.GetConnectState()
        if state == 0:
            click.echo('Logging in...')
        else:
            click.echo('Already logged in.')
        context.EnsureConnected()
        gubun = context.GetServerGubun()
        if gubun == '1':
            click.echo('Logged into Simulation server.')
        else:
            click.echo('Logged into Real server.')

@cli.group(context_settings=CONTEXT_SETTINGS, short_help='Configure many things.')
def config():
    pass

@config.command(context_settings=CONTEXT_SETTINGS, short_help='Configure auto login.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def autologin(port, verbose):
    set_verbosity(verbose)
    from koapy import KiwoomOpenApiContext
    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout) as context:
        context.EnsureConnected()
        context.ShowAccountWindow()

@cli.group(context_settings=CONTEXT_SETTINGS, short_help='Update openapi metadata.')
def update():
    pass

@update.command(context_settings=CONTEXT_SETTINGS, short_help='Update openapi TR metadata.')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def trdata(verbose):
    set_verbosity(verbose)
    from koapy.openapi.TrInfo import TrInfo
    TrInfo.dump_trinfo_by_code()

@update.command(context_settings=CONTEXT_SETTINGS, short_help='Update openapi realtype metadata.')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def realdata(verbose):
    set_verbosity(verbose)
    from koapy.openapi.RealType import RealType
    RealType.dump_realtype_by_desc()

@cli.group(context_settings=CONTEXT_SETTINGS, short_help='Get various types of data.')
def get():
    pass

market_codes = [
    '0',
    '10',
    '3',
    '8',
    '50',
    '4',
    '5',
    '6',
    '9',
    '30',
    'all',
]

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get stock codes.')
@click.option('-m', '--market', 'markets', metavar='MARKET', multiple=True, type=click.Choice(market_codes, case_sensitive=False), help='Stock market code to get. Can set multiple times.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
def stockcode(markets, port):
    """
    \b
    Possible market codes are:
      0 : 장내
      10 : 코스닥
      3 : ELW
      8 : ETF
      50 : KONEX
      4 : 뮤추얼펀드
      5 : 신주인수권
      6 : 리츠
      9 : 하이얼펀드
      30 : K-OTC

    \b
    Possible market code aliases are:
      all: All possible market codes.
    """

    if (markets) == (tuple()):
        fail_with_usage()

    from koapy import KiwoomOpenApiContext

    if 'all' in markets:
        markets = market_codes

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout) as context:
        context.EnsureConnected()

        codes = set()

        for market in markets:
            codes = codes.union(set(context.GetCodeListByMarketAsList(market)))

        codes = sorted(list(codes))

        for code in codes:
            click.echo(code)

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get name for stock codes.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
def stockname(codes, port):
    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout) as context:
        context.EnsureConnected()

        def get_codes():
            if codes:
                if '-' in codes:
                    with click.open_file('-', 'r') as f:
                        for code in f:
                            yield code.strip()
                else:
                    for code in codes:
                        yield code
            else:
                while True:
                    try:
                        code = click.prompt('code', prompt_suffix=' >>> ')
                        code = code.strip()
                        if code == 'exit':
                            break
                        if code:
                            yield code
                    except EOFError:
                        break

        for code in get_codes():
            name = context.GetMasterCodeName(code)
            click.echo(name)

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get basic information of stocks.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-m', '--market', 'markets', metavar='MARKET', multiple=True, type=click.Choice(market_codes, case_sensitive=False), help='Stock market code to get. Alternative to --code. Can set multiple times.')
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --code or --market.')
@click.option('-o', '--output', metavar='FILENAME', type=click.Path(), help="Output filename. Optional for single code (prints to console).")
@click.option('-f', '--format', metavar='FORMAT', type=click.Choice(['md', 'xlsx', 'json'], case_sensitive=False))
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def stockinfo(codes, markets, input, output, format, port, verbose): # pylint: disable=redefined-builtin
    """
    \b
    Possible market codes are:
      0 : 장내
      10 : 코스닥
      3 : ELW
      8 : ETF
      50 : KONEX
      4 : 뮤추얼펀드
      5 : 신주인수권
      6 : 리츠
      9 : 하이얼펀드
      30 : K-OTC

    \b
    Possible market code aliases are:
      all: All possible market codes.
    """

    if (codes, markets, input, output) == (tuple(), tuple(), None, None):
        fail_with_usage()

    set_verbosity(verbose)

    codes_from_input = False
    codes_len = len(codes)

    if codes_len == 0 and len(markets) == 0:
        if input is None:
            fail_with_usage('Cannot specify codes.')
        if not os.path.exists(input):
            fail_with_usage('Given input does not exist.')

        codes_from_input = True

        if os.path.isfile(input):
            if input.endswith('.xlsx'):
                import pandas as pd
                df = pd.read_excel(input, dtype=str)
                code_column = '종목코드'
                if code_column in df:
                    codes = df[code_column]
                else:
                    codes = df.iloc[0]
                codes_len = len(codes)
            elif input.endswith('.txt'):
                with open(input) as f:
                    codes = [line.strip() for line in f]
                codes_len = len(codes)
            else:
                fail_with_usage('Unrecognized input type.')
        else:
            fail_with_usage('Unrecognized input type.')

    if output is None:
        if codes_len > 1 or codes_from_input:
            fail_with_usage('Output path is not specified.')
        if format is None:
            format = 'md'
    else:
        if format is None:
            format = 'xlsx'
        if format == 'xlsx':
            if not output.endswith('.xlsx'):
                output += '.xlsx'
        elif format == 'md':
            if not output.endswith('.md'):
                output += '.md'
        elif format == 'json':
            if not output.endswith('.json'):
                output += '.json'

    import pandas as pd

    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        if not codes_from_input and codes_len == 1:
            df = context.GetStockInfoAsDataFrame(codes)
            if not output:
                if format == 'md':
                    click.echo(df.iloc[0].to_markdown())
                elif format == 'json':
                    click.echo(df.iloc[0].to_json())
            else:
                if format == 'xlsx':
                    df.to_excel(output, index=False)
                elif format == 'json':
                    with open(output, 'w') as f:
                        click.echo(df.iloc[0].to_json(), file=f)
        elif codes_len > 0:
            df = context.GetStockInfoAsDataFrame(codes)
            df.to_excel(output, index=False)
        elif len(markets) > 0:
            if 'all' in markets:
                markets = market_codes
            if format == 'xlsx':
                with pd.ExcelWriter(output) as writer: # pylint: disable=abstract-class-instantiated
                    for market in markets:
                        codes = context.GetCodeListByMarketAsList(market)
                        df = context.GetStockInfoAsDataFrame(codes)
                        df.to_excel(writer, index=False, sheet_name=market)
            elif format == 'json':
                codes = set()
                for market in markets:
                    codes = codes.union(set(context.GetCodeListByMarketAsList(market)))
                codes = sorted(list(codes))
                with open(output, 'w', encoding='utf-8') as f:
                    for code in codes:
                        df = context.GetStockInfoAsDataFrame(code)
                        click.echo(df.iloc[0].to_json(), file=f)
        else:
            fail_with_usage('Cannot specify codes.')

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get daily OHLCV of stocks.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --codes option.')
@click.option('-o', '--output', metavar='FOLDER|FILENAME', type=click.Path(), help='Output foldername or filename for single code. Files inside the folder would be named as CODE.xlsx. Defaults to current directory.')
@click.option('-s', '--start-date', metavar='YYYY-MM-DD', type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d']), help='Most recent date to get. Defaults to today or yesterday if market is open.')
@click.option('-e', '--end-date', metavar='YYYY-MM-DD', type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d']), help='Stops if reached, not included (optional).')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def daily(codes, input, output, start_date, end_date, port, verbose): # pylint: disable=redefined-builtin
    if (codes, input, output, start_date, end_date) == (tuple(), None, None, None, None):
        fail_with_usage()

    set_verbosity(verbose)

    codes_len = len(codes)

    if codes_len == 0:
        if input is None:
            fail_with_usage('Either code or input should be given.')
        if not os.path.exists(input):
            fail_with_usage('Given input does not exist.')

        if os.path.isfile(input):
            if input.endswith('.xlsx'):
                import pandas as pd
                df = pd.read_excel(input, dtype=str)
                code_column = '종목코드'
                if code_column in df:
                    codes = df[code_column]
                else:
                    codes = df.iloc[0]
                codes_len = len(codes)
            elif input.endswith('.txt'):
                with open(input) as f:
                    codes = [line.strip() for line in f]
                codes_len = len(codes)
            else:
                fail_with_usage('Unrecognized input type.')
        elif os.path.isdir(input):
            import re
            codes = [os.path.splitext(name)[0] for name in os.listdir(input) if name.endswith('.xlsx')]
            codes = [code for code in codes if re.match(r'[0-9A-Z]+', code)]
            codes_len = len(codes)
        else:
            fail_with_usage('Unrecognized input type.')

    if output is None:
        output = '.'

    if os.path.exists(output):
        if os.path.isdir(output):
            output_is_folder = True
        else:
            output_is_folder = False
    else:
        if output.endswith('/') or output.endswith(os.path.sep) or codes_len > 1:
            output_is_folder = True
        else:
            output_is_folder = False

    if output_is_folder:
        def filepath_for_code(code):
            if not os.path.exists(output):
                os.mkdir(output)
            return os.path.relpath(os.path.join(output, code + '.xlsx'))
    else:
        if not output.endswith('.xlsx'):
            output += '.xlsx'
        def filepath_for_code(_):
            return output

    import datetime
    import pandas as pd

    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        for i, code in enumerate(codes):
            logging.info('Starting to get stock data for code: %s (%d/%d)', code, i+1, codes_len)
            filepath = filepath_for_code(code)
            appended = False
            if os.path.exists(filepath):
                df = pd.read_excel(filepath, dtype=str)
                if df.shape[0] > 0:
                    last_date = df.loc[0, '일자']
                    last_date = datetime.datetime.strptime(last_date, '%Y%m%d')
                    logging.info('Found existing file %s, prepending from %s until %s', os.path.basename(filepath), start_date, last_date)
                    df = pd.concat([context.GetDailyStockDataAsDataFrame(code, start_date, last_date), df], sort=False)
                    tempfilepath = filepath + '.tmp'
                    df.to_excel(tempfilepath, index=False)
                    os.replace(tempfilepath, filepath)
                    appended = True
            if not appended:
                df = context.GetDailyStockDataAsDataFrame(code, start_date, end_date)
                df.to_excel(filepath, index=False)
            logging.info('Saved stock data for code %s to %s', code, filepath)

minute_intervals = [
    '1',
    '3',
    '5',
    '10',
    '15',
    '30',
    '45',
    '60',
]

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get minute OHLCV of stocks.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-t', '--interval', metavar='INTERVAL', type=click.Choice(minute_intervals, case_sensitive=False), help='Minute interval. Possible values are [%s]' % '|'.join(minute_intervals))
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --codes option.')
@click.option('-o', '--output', metavar='FOLDER|FILENAME', type=click.Path(), help='Output foldername or filename for single code. Files inside the folder would be named as CODE.xlsx. Defaults to current directory.')
@click.option('-s', '--start-date', metavar="YYYY-MM-DD['T'hh:mm:ss]", type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d', '%Y-%m-%dT%H:%M:%S', '%Y%m%d%H%M%S']), help='Most recent date to get. Defaults to today or yesterday if market is open.')
@click.option('-e', '--end-date', metavar="YYYY-MM-DD['T'hh:mm:ss]", type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d', '%Y-%m-%dT%H:%M:%S', '%Y%m%d%H%M%S']), help='Stops if reached, not included (optional).')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def minute(codes, interval, input, output, start_date, end_date, port, verbose): # pylint: disable=redefined-builtin
    if (codes, interval, input, output, start_date, end_date) == (tuple(), None, None, None, None, None):
        fail_with_usage()

    set_verbosity(verbose)

    if interval is None:
        fail_with_usage('Interval is not set.')

    codes_len = len(codes)

    if codes_len == 0:
        if input is None:
            fail_with_usage('Either code or input should be given.')
        if not os.path.exists(input):
            fail_with_usage('Given input does not exist.')

        if os.path.isfile(input):
            if input.endswith('.xlsx'):
                import pandas as pd
                df = pd.read_excel(input, dtype=str)
                code_column = '종목코드'
                if code_column in df:
                    codes = df[code_column]
                else:
                    codes = df.iloc[0]
                codes_len = len(codes)
            elif input.endswith('.txt'):
                with open(input) as f:
                    codes = [line.strip() for line in f]
                codes_len = len(codes)
            else:
                fail_with_usage('Unrecognized input type.')
        elif os.path.isdir(input):
            import re
            codes = [os.path.splitext(name)[0] for name in os.listdir(input) if name.endswith('.xlsx')]
            codes = [code for code in codes if re.match(r'[0-9A-Z]+', code)]
            codes_len = len(codes)
        else:
            fail_with_usage('Unrecognized input type.')

    if output is None:
        output = '.'

    if os.path.exists(output):
        if os.path.isdir(output):
            output_is_folder = True
        else:
            output_is_folder = False
    else:
        if output.endswith('/') or output.endswith(os.path.sep) or codes_len > 1:
            output_is_folder = True
        else:
            output_is_folder = False

    if output_is_folder:
        def filepath_for_code(code):
            if not os.path.exists(output):
                os.mkdir(output)
            return os.path.relpath(os.path.join(output, code + '.xlsx'))
    else:
        if not output.endswith('.xlsx'):
            output += '.xlsx'
        def filepath_for_code(_):
            return output

    import datetime
    import pandas as pd

    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        for i, code in enumerate(codes):
            logging.info('Starting to get stock data for code: %s (%d/%d)', code, i+1, codes_len)
            filepath = filepath_for_code(code)
            appended = False
            if os.path.exists(filepath):
                df = pd.read_excel(filepath, dtype=str)
                if df.shape[0] > 0:
                    last_date = df.loc[0, '체결시간']
                    last_date = datetime.datetime.strptime(last_date, '%Y%m%d%H%M%S')
                    logging.info('Found existing file %s, prepending from %s until %s', os.path.basename(filepath), start_date, last_date)
                    df = pd.concat([context.GetMinuteStockDataAsDataFrame(code, interval, start_date, last_date), df], sort=False)
                    tempfilepath = filepath + '.tmp'
                    df.to_excel(tempfilepath, index=False)
                    os.replace(tempfilepath, filepath)
                    appended = True
            if not appended:
                df = context.GetMinuteStockDataAsDataFrame(code, interval, start_date, end_date)
                df.to_excel(filepath, index=False)
            logging.info('Saved stock data for code %s to %s', code, filepath)

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get TR info.')
@click.option('-t', '--trcode', 'trcodes', metavar='TRCODE', multiple=True, help='TR code to get (like opt10001).')
def trinfo(trcodes):
    from koapy.openapi.TrInfo import TrInfo

    def get_codes():
        if trcodes:
            if '-' in trcodes:
                with click.open_file('-', 'r') as f:
                    for code in f:
                        yield code.strip()
            else:
                for code in trcodes:
                    yield code
        else:
            while True:
                try:
                    code = click.prompt('trcode', prompt_suffix=' >>> ')
                    code = code.strip()
                    if code == 'exit':
                        break
                    if code:
                        yield code
                except EOFError:
                    break

    for trcode in get_codes():
        if not trcode.startswith('opt'):
            trcode = 'opt' + trcode
        trinfo = TrInfo.get_trinfo_by_code(trcode)
        click.echo('[%s] : [%s]' % (trinfo.tr_code.upper(), trinfo.name))
        click.echo('  [INPUT]')
        for input in trinfo.inputs:
            click.echo('    %s' % input.name)
        if trinfo.single_outputs:
            click.echo('  [OUTPUT] [SINGLE DATA] : [%s]' % trinfo.single_outputs_name)
            for output in trinfo.single_outputs:
                click.echo('    %s' % output.name)
        if trinfo.multi_outputs:
            click.echo('  [OUTPUT] [MULTI DATA]  : [%s]' % trinfo.multi_outputs_name)
            for output in trinfo.multi_outputs:
                click.echo('    %s' % output.name)

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get real type info.')
@click.option('-t', '--realtype', 'realtypes', metavar='REALTYPE', multiple=True, help='Real type name to get (like 주식시세).')
def realinfo(realtypes):
    from koapy.openapi.RealType import RealType

    def get_realtypes():
        if realtypes:
            if '-' in realtypes:
                with click.open_file('-', 'r') as f:
                    for realtype in f:
                        yield realtype.strip()
            else:
                for realtype in realtypes:
                    yield realtype
        else:
            while True:
                try:
                    realtype = click.prompt('realtype', prompt_suffix=' >>> ')
                    realtype = realtype.strip()
                    if realtype == 'exit':
                        break
                    if realtype:
                        yield realtype
                except EOFError:
                    break

    for realtype in get_realtypes():
        fids = RealType.get_fids_by_realtype(realtype)
        if fids:
            names = [RealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
            for fid, name in zip(fids, names):
                click.echo('  [%s] = %s' % (fid, name))

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get market holidays.')
@click.option('-o', '--output', metavar='FILENAME', type=click.Path(), help='Output filename. (optional)')
@click.option('-O', '--offline', is_flag=True, help='Do not use krx marketdata api. (default: false)')
@click.option('-u', '--update', is_flag=True, help='Update local cache, download from krx marketdata api.')
@click.option('-U', '--no-update', is_flag=True, help='Disable update.')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def holidays(output, offline, update, no_update, verbose):
    set_verbosity(verbose)

    if output is None:
        import pandas as pd
        if not offline:
            from koapy.utils.krx.marketdata.holiday import download_holidays_as_dict
            response = download_holidays_as_dict()
            if not no_update:
                from koapy.utils.krx.holiday.KrxBusinessDay import dump_holidays
                dump_holidays(response)
        else:
            from koapy.utils.krx.holiday import get_holidays_as_dict
            response = get_holidays_as_dict()
            if not no_update or update:
                logging.warning('Cannot update while offline.')
        lang = locale.getdefaultlocale()[0]
        if lang == 'ko_KR':
            day_key = 'kr_dy_tp'
            columns = ['일자 및 요일', '요일구분', '비고']
        else:
            day_key = 'dy_tp_cd'
            columns = ['date', 'day of week', 'comment']
        data = []
        for holiday in response['block1']:
            date = holiday['calnd_dd_dy']
            day = holiday[day_key].strip()
            name = holiday['holdy_nm']
            data.append([date, day, name])
        df = pd.DataFrame.from_records(data, columns=columns)
        click.echo(df.to_markdown())
    else:
        if not offline:
            from koapy.utils.krx.marketdata.holiday import download_holidays_as_excel
            if output and not output.endswith('.xls'):
                output += '.xls'
            download_holidays_as_excel(output)
            if update:
                logging.warning('Cannot update on file output.')
        else:
            fail_with_usage('Saving to file should come with offline option disabled.')

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get user information.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def userinfo(port, verbose):
    set_verbosity(verbose)

    import pandas as pd
    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        result = {}
        result['보유계좌수'] = context.GetLoginInfo('ACCOUNT_CNT')
        account_numbers = context.GetLoginInfo('ACCLIST').rstrip(';').split(';')
        for i, accno in enumerate(account_numbers):
            result['계좌번호 (%d/%s)' % (i + 1, result['보유계좌수'])] = accno
        result['사용자 ID'] = context.GetLoginInfo('USER_ID')
        result['사용자 명'] = context.GetLoginInfo('USER_NAME')
        result['키보드보안 해지 여부'] = {
            '0': '정상',
            '1': '해지',
        }.get(context.GetLoginInfo('KEY_BSECGB'), '알수없음')
        result['방화벽 설정 여부'] = {
            '0': '미설정',
            '1': '설정',
            '2': '해지',
        }.get(context.GetLoginInfo('FIREW_SECGB'), '알수없음')
        result['접속서버 구분'] = {
            '1': '모의투자',
        }.get(context.GetServerGubun(), '실서버')

        click.echo(pd.Series(result).to_markdown())

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get account deposit.')
@click.option('-a', '--account', metavar='ACCNO', help='Account number.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def deposit(account, port, verbose):
    set_verbosity(verbose)

    if account is None:
        logging.info('Account not given. Using first account available.')

    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        if account is None:
            account = context.GetAccountList()[0]

        result = context.GetDepositInfo(account)
        click.echo(result.to_markdown())

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get account evaluation.')
@click.option('-a', '--account', metavar='ACCNO', help='Account number.')
@click.option('-d', '--include-delisted', is_flag=True, help='Include delisted.', default=True)
@click.option('-D', '--exclude-delisted', is_flag=True, help='Exclude delisted.')
@click.option('-e', '--for-each', is_flag=True, help='Show individual evaluation.', default=True)
@click.option('-E', '--as-summary', is_flag=True, help='Show summarized evaluation.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def evaluation(account, include_delisted, exclude_delisted, for_each, as_summary, port, verbose):
    set_verbosity(verbose)

    if account is None:
        logging.info('Account not given. Using first account available.')

    if exclude_delisted:
        include_delisted = False

    if as_summary:
        for_each = False
        lookup_type = '1'
    elif for_each:
        lookup_type = '2'

    from koapy import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        if account is None:
            account = context.GetAccountList()[0]

        single, multi = context.GetAccountEvaluationStatusAsSeriesAndDataFrame(account, include_delisted)
        click.echo('[계좌평가현황요청] : [계좌평가현황]')
        click.echo(single.to_markdown())
        click.echo()
        click.echo('[계좌평가현황요청] : [종목별계좌평가현황]')
        click.echo(multi.to_markdown())
        click.echo()

        single, multi = context.GetAccountEvaluationBalanceAsSeriesAndDataFrame(account, lookup_type)
        click.echo('[계좌평가잔고내역요청] : [계좌평가결과]')
        click.echo(single.to_markdown())
        click.echo()
        click.echo('[계좌평가잔고내역요청] : [계좌평가잔고개별합산]')
        click.echo(multi.to_markdown())

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get order history of a date.')
@click.option('-a', '--account', metavar='ACCNO', help='Account number.')
@click.option('-d', '--date', metavar='DATE', help='Date to get.')
@click.option('-r', '--reverse', is_flag=True)
@click.option('-e', '--executed-only', is_flag=True)
@click.option('-E', '--not-executed-only', is_flag=True)
@click.option('-S', '--stock-only', is_flag=True)
@click.option('-B', '--bond-only', is_flag=True)
@click.option('-s', '--sell-only', is_flag=True)
@click.option('-b', '--buy-only', is_flag=True)
@click.option('-c', '--code', metavar='CODE', help='Stock code to get.')
@click.option('-o', '--starting-order-no', metavar='ORDERNO', help='Starting order no.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def orders(account, date, reverse, executed_only, not_executed_only, stock_only, bond_only, sell_only, buy_only, code, starting_order_no, port, verbose):
    set_verbosity(verbose)

    if account is None:
        logging.info('Account not given. Using first account available.')

    from koapy import KiwoomOpenApiContext

    sort_type = '1'
    if reverse:
        sort_type = '2'
    if executed_only:
        sort_type = '3'
    if not_executed_only:
        sort_type = '4'
    asset_type = '0'
    if stock_only:
        asset_type = '1'
    if bond_only:
        asset_type = '2'
    order_type = '0'
    if sell_only:
        order_type = '1'
    if buy_only:
        order_type = '2'

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        if account is None:
            account = context.GetAccountList()[0]

        click.echo(context.GetOrderLogAsDataFrame3(account, date, sort_type, asset_type, order_type, code, starting_order_no).to_markdown())

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get OpenApi module installation path.')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def modulepath(port, verbose):
    set_verbosity(verbose)
    from koapy import KiwoomOpenApiContext
    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        click.echo(context.GetAPIModulePath())

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get error message for error code.')
@click.option('-e', '--err-code', metavar='ERR', type=int, help='Error code to check.')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def errmsg(err_code, verbose):
    set_verbosity(verbose)
    from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
    err_msg = KiwoomOpenApiError.get_error_message_by_code(err_code)
    click.echo('[%d] %s' % (err_code, err_msg))

@cli.command(context_settings=CONTEXT_SETTINGS, short_help='Watch realtime data.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --codes option.')
@click.option('-f', '--fid', 'fids', metavar='FID', multiple=True, help='FID to get. Can set multiple times.')
@click.option('-t', '--realtype', metavar='REALTYPE', help='Real type name. Alternative to --fid.')
@click.option('-o', '--output', metavar='FILENAME', type=click.File('w', lazy=True), default='-', help='Output filename (optional).')
@click.option('-f', '--format', metavar='FORMAT', type=click.Choice(['md', 'json'], case_sensitive=False), default='md')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def watch(codes, input, fids, realtype, output, format, port, verbose):
    if (codes, fids, realtype) == (tuple(), tuple(), None):
        fail_with_usage()

    set_verbosity(verbose)

    codes_len = len(codes)

    if codes_len == 0:
        if input is None:
            fail_with_usage('Either code or input should be given.')
        if not os.path.exists(input):
            fail_with_usage('Given input does not exist.')

        if os.path.isfile(input):
            if input.endswith('.xlsx'):
                import pandas as pd
                df = pd.read_excel(input, dtype=str)
                code_column = '종목코드'
                if code_column in df:
                    codes = df[code_column]
                else:
                    codes = df.iloc[0]
                codes_len = len(codes)
            elif input.endswith('.txt'):
                with open(input) as f:
                    codes = [line.strip() for line in f]
                codes_len = len(codes)
            else:
                fail_with_usage('Unrecognized input type.')
        else:
            fail_with_usage('Unrecognized input type.')

    if realtype is not None:
        from koapy.openapi.RealType import RealType
        fids_from_realtype = RealType.get_fids_by_realtype(realtype)
        fids = list(set(fids).union(set(fids_from_realtype)))

    if not codes:
        fail_with_usage('No codes to watch. Set --code or --input.')

    if not fids:
        fail_with_usage('Cannot infer fids to watch. Set either --fid or --realtype.')

    import datetime
    import pandas as pd

    from koapy import KiwoomOpenApiContext
    from koapy.openapi.RealType import RealType

    def parse_message(message):
        fids = event.listen_response.single_data.names
        names = [RealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
        values = event.listen_response.single_data.values
        dic = dict((name, value) for fid, name, value in zip(fids, names, values) if name != fid)
        series = pd.Series(dic)
        return series

    if format == 'json':
        def print_message(message):
            click.echo(parse_message(message).to_json(), file=output)
    else:
        def print_message(message):
            code = event.listen_response.arguments[0].string_value
            name = event.listen_response.arguments[1].string_value
            click.echo('[%s] [%s]' % (code, name), file=output)
            click.echo('[%s]' % datetime.datetime.now(), file=output)
            click.echo(parse_message(message).to_markdown(), file=output)

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        for event in context.WatchRealDataForCodesAsStream(codes, fids, infer_fids=True):
            print_message(event)

order_types = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
]

quote_types = [
    '00',
    '03',
    '05',
    '06',
    '07',
    '10',
    '13',
    '16',
    '20',
    '23',
    '26',
    '61',
    '62',
    '81',
]

@cli.command(context_settings=CONTEXT_SETTINGS, short_help='Place an order.')
@click.option('--request-name', metavar='NAME')
@click.option('--screen-no', metavar='SCRNO')
@click.option('--account-no', metavar='ACCNO')
@click.option('--order-type', type=click.Choice(order_types))
@click.option('--code', metavar='CODE')
@click.option('--quantity', metavar='QTY')
@click.option('--price', metavar='PRICE')
@click.option('--quote-type', type=click.Choice(quote_types))
@click.option('--original-order-no', metavar='ORDERNO')
@click.option('-f', '--format', metavar='FORMAT', type=click.Choice(['pretty', 'json'], case_sensitive=False))
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def order(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no, format, port, verbose):
    """
    \b
    [주문유형]
      1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정

    \b
    [거래구분]
      모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

    \b
      00 : 지정가
      03 : 시장가
      05 : 조건부지정가
      06 : 최유리지정가
      07 : 최우선지정가
      10 : 지정가IOC
      13 : 시장가IOC
      16 : 최유리IOC
      20 : 지정가FOK
      23 : 시장가FOK
      26 : 최유리FOK
      61 : 장전시간외종가
      62 : 시간외단일가매매
      81 : 장후시간외종가
    """

    if (request_name, screen_no, account_no, order_type, code, quantity) == (None, None, None, None, None, None):
        fail_with_usage()

    set_verbosity(verbose)

    from koapy import KiwoomOpenApiContext
    from google.protobuf.json_format import MessageToDict

    if format == 'json':
        import json
        def print_message(message):
            click.echo(json.dumps(MessageToDict(message)))
    else:
        import pprint
        pp = pprint.PrettyPrinter()
        def print_message(message):
            click.echo(pp.pformat(MessageToDict(message)))

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()
        for response in context.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no):
            print_message(response)

if __name__ == '__main__':
    cli()
