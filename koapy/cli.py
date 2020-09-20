"""Console script for koapy."""

import os
import logging

import click
import koapy

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
@click.argument('args', nargs=-1)
def serve(port, args):
    """
    ARGS are passed to QApplication.
    """
    args = ['--port', port] + list(args)
    from koapy.pyqt5.KiwoomOpenApiTrayApplication import KiwoomOpenApiTrayApplication
    KiwoomOpenApiTrayApplication.main(args)

@cli.group(short_help='Get several types of data.')
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
@get.command(context_settings=CONTEXT_SETTINGS, short_help='Get basic information of stocks.')
@click.option('-c', '--code', 'codes', metavar='CODE', multiple=True, help='Stock code to get. Can set multiple times.')
@click.option('-m', '--market', 'markets', metavar='MARKET', multiple=True, type=click.Choice(market_codes, case_sensitive=False), help='Stock market code to get. Alternative to --code. Can set multiple times.')
@click.option('-i', '--input', metavar='FILENAME', type=click.Path(), help='Text or excel file containing codes. Alternative to --code or --market.')
@click.option('-o', '--output', metavar='FILENAME', type=click.Path(), help="Output filename. Optional for single code (prints to console).")
@click.option('-p', '--port', metavar='PORT', help='Port number of grpc server (optional).')
def info(codes, markets, input, output, port):
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

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout) as context:
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
def daily(codes, input, output, start_date, end_date, port):
    if (codes, input, output, start_date, end_date) == (tuple(), None, None, None, None):
        fail_with_usage()

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
            codes = [code for code in codes if re.match(r'[0-9A-Z]{6}', code)]
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

    with KiwoomOpenApiContext(port=port, client_check_timeout=client_check_timeout) as context:
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

if __name__ == '__main__':
    cli()
