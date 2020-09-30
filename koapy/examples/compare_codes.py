import pandas as pd

from koapy import KiwoomOpenApiContext
from koapy.backend.cybos.CybosPlusComObject import CybosPlusComObject

kiwoom = KiwoomOpenApiContext()
cybos = CybosPlusComObject()

kiwoom.EnsureConnected()
cybos.EnsureConnected()

kiwoom_codes = kiwoom.GetCommonCodeList()
cybos_codes = cybos.GetCommonCodeList()

cybos_codes = [code[1:] for code in cybos_codes]

kiwoom_codes = pd.DataFrame(kiwoom_codes, columns=['code'])
kiwoom_codes['kiwoom'] = 'TRUE'
cybos_codes = pd.DataFrame(cybos_codes, columns=['code'])
cybos_codes['cybos'] = 'TRUE'

df = pd.merge(kiwoom_codes, cybos_codes, how='outer', on='code')

df.to_excel('output.xlsx')
