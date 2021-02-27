# Test this example script with two different scenarios
#
# 1. External-Server-Process scenario
#   1. Run 04_koapy_tray_application.py script in 32bit environment
#       => Server will start with tray application
#   2. Open another console and run 05_koapy_entrypoint.py script (this one), in 32bit or 64bit environment
#       => Client will connect to the existing server
#
# 2. Server-In-Subprocess scenario
#   1. Just run 05_koapy_entrypoint.py script (this one) in 32bit environment
#       => Server will start in subprocess and Client will connect to it

from koapy import KiwoomOpenApiPlusEntrypoint

entrypoint = KiwoomOpenApiPlusEntrypoint()

APIModulePath = entrypoint.GetAPIModulePath()

print(APIModulePath)
