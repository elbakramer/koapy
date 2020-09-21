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
@click.option('-v', '--verbose', count=True, default=3, help='Verbosity.')
@click.argument('args', nargs=-1)
def serve(port, verbose, args):
    """
    ARGS are passed to QApplication.
    """
    args = ['--port', port]
    if verbose > 0:
        args.append('-' + 'v' * verbose)
    args += list(args)
    from koapy.pyqt5.KiwoomOpenApiTrayApplication import KiwoomOpenApiTrayApplication
    KiwoomOpenApiTrayApplication.main(args)

@cli.group(short_help='Get various types of data.')
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
def code(markets, port):
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

    from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext

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
def name(codes, port):
    from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext

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
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def info(codes, markets, input, output, port, verbose):
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
                df = pd.read_excel(input, dtype='object')
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
    else:
        if not output.endswith('.xlsx'):
            output += '.xlsx'

    import pandas as pd

    from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        if not codes_from_input and codes_len == 1:
            df = context.GetStockInfoAsDataFrame(codes)
            if not output:
                click.echo(df.iloc[0].to_markdown())
            else:
                df.to_excel(output, index=False)
        elif codes_len > 0:
            df = context.GetStockInfoAsDataFrame(codes)
            df.to_excel(output, index=False)
        elif len(markets) > 0:
            if 'all' in markets:
                markets = market_codes
            with pd.ExcelWriter(output) as writer: # pylint: disable=abstract-class-instantiated
                for market in markets:
                    codes = context.GetCodeListByMarketAsList(market)
                    df = context.GetStockInfoAsDataFrame(codes)
                    df.to_excel(writer, index=False, sheet_name=market)
        else:
            fail_with_usage('Cannot specify codes.')

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get daily OHLCV of stocks.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --codes option.')
@click.option('-o', '--output', metavar='FOLDER|FILENAME', type=click.Path(), help='Output foldername or filename for single code. Files inside the folder would be named as CODE.xlsx. Defaults to current directory.')
@click.option('-s', '--start-date', metavar='YYYY-MM-DD', type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d']), help='Most recent date to get. Defaults to today or yesterday if market is open.')
@click.option('-e', '--end-date', metavar='YYYY-MM-DD', type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d']), help='Oldest date to get (optional).')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def daily(codes, input, output, start_date, end_date, port, verbose):
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
                df = pd.read_excel(input, dtype='object')
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
            return os.path.join(output, code + '.xlsx')
    else:
        if not output.endswith('.xlsx'):
            output += '.xlsx'
        def filepath_for_code(_):
            return output

    import datetime
    import pandas as pd

    from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        for i, code in enumerate(codes):
            logging.info('Starting to get stock data for code: %s (%d/%d)', code, i+1, codes_len)
            filepath = filepath_for_code(code)
            if os.path.exists(filepath):
                df = pd.read_excel(filepath, dtype='object')
                last_date = df.loc[0, '일자']
                last_date = datetime.datetime.strptime(last_date, '%Y%m%d')
                logging.info('Found existing file %s, prepending from %s until %s', os.path.basename(filepath), start_date, last_date)
                df = pd.concat([context.GetDailyStockDataAsDataFrame(code, start_date, last_date), df], sort=False)
            else:
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
@click.option('-s', '--start-date', metavar='YYYY-MM-DD', type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d']), help='Most recent date to get. Defaults to today or yesterday if market is open.')
@click.option('-e', '--end-date', metavar='YYYY-MM-DD', type=click.DateTime(formats=['%Y-%m-%d', '%Y%m%d']), help='Oldest date to get (optional).')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def minute(codes, interval, input, output, start_date, end_date, port, verbose):
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
                df = pd.read_excel(input, dtype='object')
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
            return os.path.join(output, code + '.xlsx')
    else:
        if not output.endswith('.xlsx'):
            output += '.xlsx'
        def filepath_for_code(_):
            return output

    import datetime
    import pandas as pd

    from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        for i, code in enumerate(codes):
            logging.info('Starting to get stock data for code: %s (%d/%d)', code, i+1, codes_len)
            filepath = filepath_for_code(code)
            if os.path.exists(filepath):
                df = pd.read_excel(filepath, dtype='object')
                last_date = df.loc[0, '체결시간']
                last_date = datetime.datetime.strptime(last_date, '%Y%m%d')
                logging.info('Found existing file %s, prepending from %s until %s', os.path.basename(filepath), start_date, last_date)
                df = pd.concat([context.GetMinuteStockDataAsDataFrame(code, interval, start_date, last_date), df], sort=False)
            else:
                df = context.GetMinuteStockDataAsDataFrame(code, interval, start_date, end_date)
            df.to_excel(filepath, index=False)
            logging.info('Saved stock data for code %s to %s', code, filepath)

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get TR info.')
@click.option('-t', '--trcode', 'trcodes', metavar='TRCODE', multiple=True, help='TR code to get (like opt100001).')
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
        trinfo = TrInfo.get_trinfo_by_code(trcode)
        click.echo('%s : %s' % (trinfo.tr_code, trinfo.name))
        click.echo('[INPUT]')
        for input in trinfo.inputs:
            click.echo('  %s' % input.name)
        click.echo('[OUTPUT]')
        if trinfo.single_outputs:
            click.echo('  SINGLE DATA [%s]' % trinfo.single_outputs_name)
            for output in trinfo.single_outputs:
                click.echo('    %s' % output.name)
        if trinfo.multi_outputs:
            click.echo('  MULTI DATA  [%s]' % trinfo.multi_outputs_name)
            for output in trinfo.multi_outputs:
                click.echo('    %s' % output.name)

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get Real type info.')
@click.option('-r', '--realtype', 'realtypes', metavar='REALTYPE', multiple=True, help='Real type name to get (like 주식시세).')
def realtype(realtypes):
    from koapy.openapi.RealType import RealType

    def get_realtypes():
        if realtypes:
            if '-' in realtypes:
                with click.open_file('-', 'r') as f:
                    for realtype in f:
                        yield code.strip()
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

@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get market closing dates.')
@click.option('-o', '--output', metavar='FILENAME', type=click.Path(), help='Output filename (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def closing(output, verbose):
    set_verbosity(verbose)
    if output is None:
        import pandas as pd
        from koapy.utils.krx.closing import get_krx_closing_dates_as_dict
        response = get_krx_closing_dates_as_dict()
        lang = locale.getdefaultlocale()[0]
        if lang == 'ko_KR':
            day_key = 'kr_dy_tp'
            columns = ['일자 및 요일', '요일구분', '비고']
        else:
            day_key = 'dy_tp_cd'
            columns = ['date', 'day of week', 'comment']
        data = []
        for closing_date in response['block1']:
            date = closing_date['calnd_dd_dy']
            day = closing_date[day_key].strip()
            name = closing_date['holdy_nm']
            data.append([date, day, name])
        df = pd.DataFrame.from_records(data, columns=columns)
        click.echo(df.to_markdown())
    else:
        from koapy.utils.krx.closing import download_krx_closing_dates_as_excel
        if output and not output.endswith('.xls'):
            output += '.xls'
        download_krx_closing_dates_as_excel(output)

@cli.command(context_settings=CONTEXT_SETTINGS, short_help='Watch realtime data.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --codes option.')
@click.option('-f', '--fid', 'fids', metavar='FID', multiple=True, help='FID to get. Can set multiple times.')
@click.option('-r', '--realtype', metavar='REALTYPE', help='Real type name. Alternative to --fid.')
@click.option('-o', '--output', metavar='FILENAME', type=click.File('w', lazy=True), default='-', help='Output filename (optional).')
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
@click.option('-v', '--verbose', count=True, help='Verbosity.')
def watch(codes, input, fids, realtype, output, port, verbose):
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
                df = pd.read_excel(input, dtype='object')
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

    if realtype is not None:
        from koapy.openapi.RealType import RealType
        fids = list(fids) + RealType.get_fids_by_realtype(realtype)

    if not codes:
        fail_with_usage('No codes to watch. Set --code or --input.')

    if not fids:
        fail_with_usage('Cannot infer fids to watch. Set either --fid or --realtype.')

    import datetime
    import pandas as pd

    from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext
    from koapy.openapi.RealType import RealType

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout, verbosity=verbose) as context:
        context.EnsureConnected()

        for event in context.WatchRealDataForCodesAsStream(codes, fids, infer_fids=True):
            code = event.listen_response.arguments[0].string_value
            name = event.listen_response.arguments[1].string_value
            fids = event.listen_response.single_data.names
            names = [RealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
            values = event.listen_response.single_data.values
            dic = dict((name, value) for fid, name, value in zip(fids, names, values) if name != fid)
            series = pd.Series(dic)
            click.echo('[%s]' % datetime.datetime.now(), file=output)
            click.echo('[%s] [%s]' % (code, name), file=output)
            click.echo(series.to_markdown(), file=output)

if __name__ == '__main__':
    cli()
