import click

from .account_data.deposit import deposit
from .account_data.evaluation import evaluation
from .account_data.orders import orders
from .account_data.userinfo import userinfo
from .chart_data.daily import daily
from .chart_data.minute import minute
from .openapi_meta.errmsg import errmsg
from .openapi_meta.modulepath import modulepath
from .openapi_meta.realinfo import realinfo
from .openapi_meta.trinfo import trinfo
from .stock_meta.codelist import codelist
from .stock_meta.stockcode import stockcode
from .stock_meta.stockinfo import stockinfo
from .stock_meta.stockname import stockname


@click.group(short_help="Get various types of data.")
def get():
    pass


get.add_command(deposit)
get.add_command(evaluation)
get.add_command(orders)
get.add_command(userinfo)

get.add_command(daily)
get.add_command(minute)

get.add_command(errmsg)
get.add_command(modulepath)
get.add_command(realinfo)
get.add_command(trinfo)

get.add_command(codelist)
get.add_command(stockcode)
get.add_command(stockinfo)
get.add_command(stockname)
