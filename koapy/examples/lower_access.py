import sys

from koapy import KiwoomOpenApiTrayApplication

app = KiwoomOpenApiTrayApplication(sys.argv)
control = app.get_control()

print(control.GetAPIModulePath())
