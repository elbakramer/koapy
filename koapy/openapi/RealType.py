import os
import json
import contextlib
import pandas as pd

class RealType(object):

    class FID(object):

        __outer_class__ = None

        FID_DUMP_FILENAME = 'fid.xlsx'
        NAME_BY_FID = {}

        def __init__(self, fid=None, name=None):
            self.fid = int(fid)
            self.name = name

        def __repr__(self):
            return '%s.%s(%r, %r)' % (
                self.__outer_class__.__name__,
                self.__class__.__name__,
                self.fid,
                self.name)

        @classmethod
        def name_by_fid_from_dump_file(cls, dump_file=None):
            if dump_file is None:
                dump_file = os.path.join(os.path.dirname(__file__), 'data', cls.FID_DUMP_FILENAME)
            df = pd.read_excel(dump_file)
            fids = [cls(pair[0], pair[1]) for pair in zip(df['fid'], df['name'])]
            result = {fid.fid: fid.name for fid in fids}
            return result

        @classmethod
        def get_name_by_fid(cls, fid, default=None):
            fid = int(fid)
            return cls.NAME_BY_FID.get(fid, default)

    REALTYPE_BY_DESC_DUMP_FILENAME = 'realtype_by_desc.json'
    REALTYPE_BY_DESC = {}

    def __init__(self, gidc=None, desc=None, nfid=None, fids=None):
        self.gidc = gidc
        self.desc = desc
        self.nfid = nfid
        self.fids = fids

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (
            self.__class__.__name__,
            self.gidc,
            self.desc,
            self.nfid,
            self.fids)

    def to_dict(self):
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, dic):
        output = cls()
        for name in output.__dict__:
            setattr(output, name, dic.get(name))
        return output

    def to_json(self, filename=None):
        if filename is None:
            return json.dumps(self.to_dict())
        else:
            with open(filename, 'w') as f:
                return json.dump(self.to_dict(), f)

    @classmethod
    def get_fids_by_realtype(cls, realtype):
        result = cls.REALTYPE_BY_DESC.get(realtype)
        if result is not None:
            return result.fids
        return None

    @classmethod
    def get_fids_by_realtype_as_string(cls, realtype):
        fids = cls.get_fids_by_realtype(realtype)
        if fids is not None:
            fids = [str(fid) for fid in fids]
            fids = ';'.join(fids)
        return fids

    @classmethod
    def get_field_names_by_realtype(cls, realtype):
        fids = cls.get_fids_by_realtype(realtype)
        if fids is not None:
            names = [cls.FID.get_name_by_fid(fid, str(fid)) for fid in fids]
            return names
        return None

    @classmethod
    def realtypes_from_datfile(cls, f=None, encoding='euc-kr'):
        gidc_width = 2
        desc_width = 20
        nfid_width = 3
        fid_width = 5
        if f is None:
            f = r'C:\OpenAPI\data\nkrealtime.dat'
        with contextlib.ExitStack() as stack:
            if isinstance(f, str):
                f = stack.enter_context(open(f, 'rb'))
            lines = iter(f)
            lines = map(lambda line: line.rstrip(b'\r\n'), lines)
            lines = filter(lambda line: not line.startswith(b';'), lines)
            realtypes = []
            for line in lines:
                gidc = line[:gidc_width]
                line = line[gidc_width:]
                gidc = gidc.decode(encoding).strip()
                desc = line[:desc_width]
                line = line[desc_width:]
                desc = desc.decode(encoding).strip()
                nfid = line[:nfid_width]
                nfid = nfid.strip()
                line = line[nfid_width:]
                if len(nfid) > 0:
                    nfid = int(nfid)
                else:
                    nfid = 0
                fids = []
                for _ in range(nfid):
                    fid = line[:fid_width]
                    line = line[fid_width:]
                    fid = int(fid)
                    fids.append(fid)
                assert len(line.rstrip(b'^M ')) == 0
                realtypes.append(cls(gidc, desc, nfid, fids))
            return realtypes

    @classmethod
    def realtype_by_desc_from_datfile(cls, f=None):
        realtypes = cls.realtypes_from_datfile(f)
        result = {realtype.desc:realtype for realtype in realtypes}
        return result

    @classmethod
    def dump_realtype_by_desc(cls, dump_file=None):
        with contextlib.ExitStack() as stack:
            if dump_file is None:
                dump_file = os.path.join(os.path.dirname(__file__), 'data', cls.REALTYPE_BY_DESC_DUMP_FILENAME)
            if isinstance(dump_file, str):
                dump_file = stack.enter_context(open(dump_file, 'w'))
            result = cls.realtype_by_desc_from_datfile()
            for tr_code in result:
                result[tr_code] = result[tr_code].to_dict()
            return json.dump(result, dump_file)

    @classmethod
    def realtype_by_desc_from_dump_file(cls, dump_file=None):
        with contextlib.ExitStack() as stack:
            if dump_file is None:
                dump_file = os.path.join(os.path.dirname(__file__), 'data', cls.REALTYPE_BY_DESC_DUMP_FILENAME)
            if isinstance(dump_file, str) and os.path.exists(dump_file) and os.stat(dump_file).st_size > 0:
                dump_file = stack.enter_context(open(dump_file, 'r'))
                result = json.load(dump_file)
                for desc in result:
                    result[desc] = cls.from_dict(result[desc])
                return result
        return {}


RealType.FID.__outer_class__ = RealType

RealType.REALTYPE_BY_DESC = RealType.realtype_by_desc_from_dump_file()
RealType.FID.NAME_BY_FID = RealType.FID.name_by_fid_from_dump_file()


def main():
    RealType.dump_realtype_by_desc()


if __name__ == '__main__':
    main()
