import sys

from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError

def main():
    codes = sys.argv[1:]
    for code in codes:
        code = int(code)
        print('[%d] %s' % (code, KiwoomOpenApiError.get_error_message_by_code(code)))

if __name__ == '__main__':
    main()
