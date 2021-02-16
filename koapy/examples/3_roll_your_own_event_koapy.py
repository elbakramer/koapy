import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QEventLoop

from koapy import KiwoomOpenApiPlusQAxWidget

app = QApplication(sys.argv)
control = KiwoomOpenApiPlusQAxWidget()

loop = QEventLoop()

def comm_connect():
    err = control.dynamicCall('CommConnect()')
    if err < 0:
        raise ValueError(err)
    loop.exec_()

def on_event_connect(errcode):
    if errcode < 0:
        raise ValueError(errcode)
    if errcode == 0:
        print('Connected!')
    control.OnEventConnect.disconnect(on_event_connect)
    loop.exit()

control.OnEventConnect.connect(on_event_connect)

comm_connect()

def get_stock_info(code):
    rqname = 'get_stock_info'
    trcode = 'opt10001'
    prevnext = 0
    screenno = '0001'
    control.dynamicCall('SetInputValue(const QString&, const QString&)', '종목코드', code)
    err = control.dynamicCall('CommRqData(const QString&, const QString&, int, const QString&)', rqname, trcode, prevnext, screenno)
    if err < 0:
        raise ValueError(err)
    loop.exec_()

code = '005930'
price = 0

def on_receive_tr_data(scrno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg):
    global price

    # single data
    index = 0
    itemname = '현재가'
    price = control.dynamicCall('GetCommData(const QString&, const QString&, int, const QString&)', trcode, recordname, index, itemname).strip()

    # multi data
    repeat_cnt = control.dynamicCall('GetRepeatCnt(const QString&, const QString&)', trcode, recordname)
    if repeat_cnt > 0:
        prices = []
        for index in range(repeat_cnt):
            price_index = control.dynamicCall('GetCommData(const QString&, const QString&, int, const QString&)', trcode, recordname, index, itemname).strip()
            prices.append(price_index)

    if prevnext not in ['', '0']:
        control.dynamicCall('SetInputValue(const QString&, const QString&)', '종목코드', code)
        err = control.dynamicCall('CommRqData(const QString&, const QString&, int, const QString&)', rqname, trcode, int(prevnext), scrno)
        if err < 0:
            raise ValueError(err)
    else:
        control.OnReceiveTrData.disconnect(on_receive_tr_data)
        loop.exit()

control.OnReceiveTrData.connect(on_receive_tr_data)
get_stock_info(code)

print(price)
