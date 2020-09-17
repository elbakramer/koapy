import sys

from koapy.openapi.TrInfo import TrInfo

def get_output_names_by_trcode(trcode):
    trinfo = TrInfo.get_trinfo_by_code(trcode)
    single = trinfo.get_single_output_names()
    multi = trinfo.get_multi_output_names()
    return single, multi

def main():
    trcodes = sys.argv[1:]
    for trcode in trcodes:
        print('%s:' % trcode)
        single, multi = get_output_names_by_trcode(trcode)
        print('- single: %r' % single)
        print('- multi: %r' % multi)
        print()

if __name__ == '__main__':
    main()
