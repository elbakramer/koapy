from __future__ import annotations

import contextlib
import json

from os import PathLike
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, TextIO, Union

import pandas as pd

from koapy.config import debug, default_encoding
from koapy.utils.logging.Logging import Logging
from koapy.utils.serialization import JsonSerializable


class KiwoomOpenApiPlusRealType(JsonSerializable, Logging):
    class Fid(JsonSerializable):

        __outer_class__ = None

        FID_DUMP_FILEDIR = Path(__file__).parent.parent / "data/metadata"
        FID_DUMP_FILENAME = "fid.csv"
        FID_DUMP_FILEPATH = FID_DUMP_FILEDIR / FID_DUMP_FILENAME
        FID_DUMP_PROCESSOR = pd.read_csv

        FID_BY_FID: Dict[int, KiwoomOpenApiPlusRealType.Fid] = {}
        FID_BY_NAME: Dict[str, KiwoomOpenApiPlusRealType.Fid] = {}

        def __init__(self, fid: Optional[int] = None, name: Optional[str] = None):
            if fid is not None and name is None:
                name = self.get_name_by_fid(fid)
            self.fid = fid
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
        def fids_from_dump_file(
            cls, dump_file: Optional[Union[str, PathLike]] = None
        ) -> Dict[int, str]:
            if dump_file is None:
                dump_file = cls.FID_DUMP_FILEPATH
            df = cls.FID_DUMP_PROCESSOR(dump_file)
            fids = [cls(pair[0], pair[1]) for pair in zip(df["fid"], df["name"])]
            return fids

        @classmethod
        def load_from_dump_file(cls, dump_file: Optional[Union[str, PathLike]] = None):
            fids = cls.fids_from_dump_file(dump_file)
            cls.FID_BY_FID = {fid.fid: fid for fid in fids}
            cls.FID_BY_NAME = {fid.name: fid for fid in fids}

        @classmethod
        def from_fid(
            cls, fid: Union[str, int]
        ) -> Optional[KiwoomOpenApiPlusRealType.Fid]:
            fid = int(fid)
            fid = cls.FID_BY_FID.get(fid)
            return fid

        @classmethod
        def from_name(cls, name: str) -> Optional[KiwoomOpenApiPlusRealType.Fid]:
            fid = cls.FID_BY_NAME.get(name)
            return fid

        @classmethod
        def get_name_by_fid(
            cls, fid: Union[str, int], default: Optional[str] = None
        ) -> Optional[str]:
            fid = cls.from_fid(fid)
            return fid.name if fid else default

    REALTYPE_BY_DESC_DUMP_FILEDIR = Path(__file__).parent.parent / "data/metadata"
    REALTYPE_BY_DESC_DUMP_FILENAME = "realtype_by_desc.json"
    REALTYPE_BY_DESC_DUMP_FILEPATH = (
        REALTYPE_BY_DESC_DUMP_FILEDIR / REALTYPE_BY_DESC_DUMP_FILENAME
    )

    REALTYPE_BY_DESC: Dict[str, KiwoomOpenApiPlusRealType] = {}

    def __init__(
        self,
        gidc: Optional[str] = None,
        desc: Optional[str] = None,
        nfid: Optional[int] = None,
        fids: Optional[List[int]] = None,
    ):
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
    def get_realtype_name_list(cls):
        return list(cls.REALTYPE_BY_DESC.keys())

    @classmethod
    def get_realtype_info_list(cls):
        return list(cls.REALTYPE_BY_DESC.values())

    @classmethod
    def get_realtype_info_by_desc(
        cls, desc: str
    ) -> Optional[KiwoomOpenApiPlusRealType]:
        return cls.REALTYPE_BY_DESC.get(desc)

    @classmethod
    def get_realtype_info_by_name(
        cls, name: str
    ) -> Optional[KiwoomOpenApiPlusRealType]:
        return cls.get_realtype_info_by_desc(name)

    @classmethod
    def get_realtype_info_by_realtype_name(
        cls, name: str
    ) -> Optional[KiwoomOpenApiPlusRealType]:
        return cls.get_realtype_info_by_name(name)

    @classmethod
    def from_name(cls, name: str) -> Optional[KiwoomOpenApiPlusRealType]:
        return cls.get_realtype_info_by_name(name)

    @classmethod
    def get_fids_by_realtype_name(cls, name: str) -> Optional[List[int]]:
        result = cls.get_realtype_info_by_realtype_name(name)
        if result is not None:
            return result.fids
        return None

    @classmethod
    def get_fids_by_realtype_name_as_string(cls, name: str) -> Optional[str]:
        fids = cls.get_fids_by_realtype_name(name)
        if fids is not None:
            fids = [str(fid) for fid in fids]
            fids = ";".join(fids)
        return fids

    @classmethod
    def get_field_names_by_realtype_name(cls, name: str) -> Optional[List[str]]:
        fids = cls.get_fids_by_realtype_name(name)
        names = None
        if fids is not None:
            names = [cls.Fid.get_name_by_fid(fid, str(fid)) for fid in fids]
        return names

    @classmethod
    def realtypes_from_datfile(
        cls,
        dat_file: Optional[Union[str, PathLike, BinaryIO]] = None,
        encoding: Optional[str] = None,
        module_path: Optional[str] = None,
    ) -> List[KiwoomOpenApiPlusRealType]:
        if dat_file is None:
            if module_path is None:
                from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLibSpec import (
                    API_MODULE_PATH,
                )

                module_path = API_MODULE_PATH
            dat_file = module_path / "data" / "nkrealtime.dat"

        if isinstance(dat_file, str):
            dat_file = Path(dat_file)

        if encoding is None:
            encoding = "euc-kr"

        gidc_width = 2
        desc_width = 20
        nfid_width = 3
        fid_width = 5

        with contextlib.ExitStack() as stack:
            if isinstance(dat_file, Path):
                if debug:
                    cls.logger.debug("Reading file %s", dat_file)
                dat_file = open(dat_file, "rb")
                dat_file = stack.enter_context(dat_file)
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
    def realtype_by_desc_from_datfile(
        cls, dat_file: Optional[Union[str, PathLike, BinaryIO]] = None
    ) -> Dict[str, KiwoomOpenApiPlusRealType]:
        realtypes = cls.realtypes_from_datfile(dat_file)
        result = {realtype.desc: realtype for realtype in realtypes}
        return result

    @classmethod
    def dump_realtype_by_desc(
        cls,
        dump_file: Optional[Union[str, PathLike, TextIO]] = None,
        dat_file: Optional[Union[str, PathLike, BinaryIO]] = None,
        encoding: Optional[str] = None,
    ):
        if dump_file is None:
            dump_file = cls.REALTYPE_BY_DESC_DUMP_FILEPATH
        if isinstance(dump_file, str):
            dump_file = Path(dump_file)
        with contextlib.ExitStack() as stack:
            if isinstance(dump_file, PathLike):
                dump_filename = dump_file
                if encoding is None:
                    encoding = default_encoding
                dump_file = open(dump_file, "w", encoding=encoding)
                dump_file = stack.enter_context(dump_file)
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
    def realtype_by_desc_from_dump_file(
        cls,
        dump_file: Optional[Union[str, PathLike, TextIO]] = None,
        encoding: Optional[str] = None,
    ) -> Dict[str, KiwoomOpenApiPlusRealType]:
        if dump_file is None:
            dump_file = cls.REALTYPE_BY_DESC_DUMP_FILEPATH
        if isinstance(dump_file, str):
            dump_file = Path(dump_file)
        with contextlib.ExitStack() as stack:
            if isinstance(dump_file, PathLike):
                if dump_file.exists() and dump_file.stat().st_size > 0:
                    if encoding is None:
                        encoding = default_encoding
                    dump_file = open(dump_file, "r", encoding=encoding)
                    dump_file = stack.enter_context(dump_file)
                else:
                    return {}
            result = json.load(dump_file)
        for desc in result:
            result[desc] = cls.from_dict(result[desc])
        return result

    @classmethod
    def load_from_dump_file(
        cls, dump_file: Optional[Union[str, PathLike, TextIO]] = None
    ):
        cls.REALTYPE_BY_DESC = cls.realtype_by_desc_from_dump_file(dump_file)
        cls.Fid.load_from_dump_file()

    @classmethod
    def load_from_datfile(
        cls, dat_file: Optional[Union[str, PathLike, BinaryIO]] = None
    ):
        cls.REALTYPE_BY_DESC = cls.realtype_by_desc_from_datfile(dat_file)
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
