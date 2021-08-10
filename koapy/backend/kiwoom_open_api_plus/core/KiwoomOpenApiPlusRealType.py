import contextlib
import json
import os

import pandas as pd

from koapy.utils.logging.Logging import Logging
from koapy.utils.serialization import JsonSerializable


class KiwoomOpenApiPlusRealType(JsonSerializable, Logging):
    class Fid(JsonSerializable):

        __outer_class__ = None

        _FID_DUMP_FILEDIR = os.path.join(os.path.dirname(__file__), "../data/metadata")
        _FID_DUMP_FILENAME = "fid.xlsx"
        _FID_DUMP_FILEPATH = os.path.join(_FID_DUMP_FILEDIR, _FID_DUMP_FILENAME)

        _NAME_BY_FID = {}

        def __init__(self, fid=None, name=None):
            self.fid = int(fid)
            self.name = name

        def __repr__(self):
            return "{}.{}({!r}, {!r})".format(
                self.__outer_class__.__name__,
                self.__class__.__name__,
                self.fid,
                self.name,
            )

        def __eq__(self, other):
            if isinstance(other, type(self)):
                return self.fid == other.fid and self.name == other.name
            return False

        @classmethod
        def name_by_fid_from_dump_file(cls, dump_file=None):
            if dump_file is None:
                dump_file = cls._FID_DUMP_FILEPATH
            df = pd.read_excel(dump_file)
            fids = [cls(pair[0], pair[1]) for pair in zip(df["fid"], df["name"])]
            result = {fid.fid: fid.name for fid in fids}
            return result

        @classmethod
        def load_from_dump_file(cls, dump_file=None):
            cls._NAME_BY_FID = cls.name_by_fid_from_dump_file(dump_file)

        @classmethod
        def get_name_by_fid(cls, fid, default=None):
            fid = int(fid)
            return cls._NAME_BY_FID.get(fid, default)

    _REALTYPE_BY_DESC_DUMP_FILEDIR = os.path.join(
        os.path.dirname(__file__), "../data/metadata"
    )
    _REALTYPE_BY_DESC_DUMP_FILENAME = "realtype_by_desc.json"
    _REALTYPE_BY_DESC_DUMP_FILEPATH = os.path.join(
        _REALTYPE_BY_DESC_DUMP_FILEDIR, _REALTYPE_BY_DESC_DUMP_FILENAME
    )

    _REALTYPE_BY_DESC = {}

    def __init__(self, gidc=None, desc=None, nfid=None, fids=None):
        self.gidc = gidc
        self.desc = desc
        self.nfid = nfid
        self.fids = fids

    def __repr__(self):
        return "{}({!r}, {!r}, {!r}, {!r})".format(
            self.__class__.__name__,
            self.gidc,
            self.desc,
            self.nfid,
            self.fids,
        )

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                self.gidc == other.gidc
                and self.desc == other.desc
                and self.nfid == other.nfid
                and self.fids == other.fids
            )
        return False

    @classmethod
    def get_realtype_info_by_realtype_name(cls, realtype):
        return cls._REALTYPE_BY_DESC.get(realtype)

    @classmethod
    def get_fids_by_realtype_name(cls, realtype):
        result = cls.get_realtype_info_by_realtype_name(realtype)
        if result is not None:
            return result.fids
        return None

    @classmethod
    def get_fids_by_realtype_name_as_string(cls, realtype):
        fids = cls.get_fids_by_realtype_name(realtype)
        if fids is not None:
            fids = [str(fid) for fid in fids]
            fids = ";".join(fids)
        return fids

    @classmethod
    def get_field_names_by_realtype_name(cls, realtype):
        fids = cls.get_fids_by_realtype_name(realtype)
        if fids is not None:
            names = [cls.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
            return names
        return None

    @classmethod
    def realtypes_from_datfile(cls, dat_file=None, encoding=None, module_path=None):
        if dat_file is None:
            if module_path is None:
                from koapy.backend.kiwoom_open_api_plus.utils.module_path import (
                    GetAPIModulePath,
                )

                module_path = GetAPIModulePath()
            dat_file = os.path.join(module_path, "data", "nkrealtime.dat")
        if encoding is None:
            encoding = "euc-kr"

        gidc_width = 2
        desc_width = 20
        nfid_width = 3
        fid_width = 5

        with contextlib.ExitStack() as stack:
            if isinstance(dat_file, str):
                cls.logger.debug("Reading file %s", dat_file)
                dat_file = stack.enter_context(open(dat_file, "rb"))
            lines = iter(dat_file)
            lines = map(lambda line: line.rstrip(b"\r\n"), lines)
            lines = filter(lambda line: not line.startswith(b";"), lines)
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
                assert len(line.rstrip(b"^M ")) == 0
                realtypes.append(cls(gidc, desc, nfid, fids))
            return realtypes

    @classmethod
    def realtype_by_desc_from_datfile(cls, dat_file=None):
        realtypes = cls.realtypes_from_datfile(dat_file)
        result = {realtype.desc: realtype for realtype in realtypes}
        return result

    @classmethod
    def dump_realtype_by_desc(cls, dump_file=None, dat_file=None):
        if dump_file is None:
            dump_file = cls._REALTYPE_BY_DESC_DUMP_FILEPATH
        with contextlib.ExitStack() as stack:
            if isinstance(dump_file, str):
                dump_filename = dump_file
                dump_file = stack.enter_context(open(dump_file, "w", encoding="utf-8"))
            else:
                dump_filename = None
            result = cls.realtype_by_desc_from_datfile(dat_file)
            for tr_code in result:
                result[tr_code] = result[tr_code].to_dict()
            if dump_filename is not None:
                cls.logger.debug("Saving realtype to %s", dump_filename)
            return json.dump(
                result,
                dump_file,
                indent=4,
                sort_keys=True,
                ensure_ascii=False,
            )

    @classmethod
    def realtype_by_desc_from_dump_file(cls, dump_file=None):
        if dump_file is None:
            dump_file = cls._REALTYPE_BY_DESC_DUMP_FILEPATH
        with contextlib.ExitStack() as stack:
            if isinstance(dump_file, str):
                if os.path.exists(dump_file) and os.path.getsize(dump_file) > 0:
                    dump_file = stack.enter_context(
                        open(dump_file, "r", encoding="utf-8")
                    )
                else:
                    return {}
            result = json.load(dump_file)
        for desc in result:
            result[desc] = cls.from_dict(result[desc])
        return result

    @classmethod
    def load_from_dump_file(cls, dump_file=None):
        cls._REALTYPE_BY_DESC = cls.realtype_by_desc_from_dump_file(dump_file)
        cls.Fid.load_from_dump_file()

    @classmethod
    def load_from_datfile(cls, dat_file=None):
        cls._REALTYPE_BY_DESC = cls.realtype_by_desc_from_datfile(dat_file)
        cls.Fid.load_from_dump_file()

    @classmethod
    def load(cls):
        try:
            cls.load_from_datfile()
        except FileNotFoundError:
            cls.load_from_dump_file()


KiwoomOpenApiPlusRealType.Fid.__outer_class__ = KiwoomOpenApiPlusRealType
KiwoomOpenApiPlusRealType.load()


def main():
    KiwoomOpenApiPlusRealType.dump_realtype_by_desc()


if __name__ == "__main__":
    main()
