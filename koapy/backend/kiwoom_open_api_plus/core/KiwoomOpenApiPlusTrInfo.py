import contextlib
import io
import json
import os
import zipfile

from koapy.utils.logging.Logging import Logging
from koapy.utils.serialization import JsonSerializable


class KiwoomOpenApiPlusTrInfo(JsonSerializable, Logging):

    _TRINFO_BY_CODE_DUMP_FILEDIR = os.path.join(
        os.path.dirname(__file__), "../data/metadata"
    )
    _TRINFO_BY_CODE_DUMP_FILENAME = "trinfo_by_code.json"
    _TRINFO_BY_CODE_DUMP_FILEPATH = os.path.join(
        _TRINFO_BY_CODE_DUMP_FILEDIR, _TRINFO_BY_CODE_DUMP_FILENAME
    )

    _TRINFO_BY_CODE = {}

    class Field(JsonSerializable):

        __outer_class__ = None

        def __init__(self, name=None, start=None, offset=None, fid=None):
            self.name = name
            self.start = start
            self.offset = offset
            self.fid = fid

        def __repr__(self):
            return "{}.{}({!r}, {!r}, {!r}, {!r})".format(
                self.__outer_class__.__name__,
                self.__class__.__name__,
                self.name,
                self.start,
                self.offset,
                self.fid,
            )

        def __eq__(self, other):
            if isinstance(other, type(self)):
                return (
                    self.name == other.name
                    and self.start == other.start
                    and self.offset == other.offset
                    and self.fid == other.fid
                )
            return False

    def __init__(
        self,
        tr_code=None,
        name=None,
        tr_name=None,
        tr_names_svr=None,
        tr_type=None,
        gfid=None,
        inputs=None,
        single_outputs_name=None,
        single_outputs=None,
        multi_outputs_name=None,
        multi_outputs=None,
    ):
        self.tr_code = tr_code
        self.name = name
        self.tr_name = tr_name
        self.tr_names_svr = tr_names_svr
        self.tr_type = tr_type
        self.gfid = gfid
        self.inputs = inputs
        self.single_outputs_name = single_outputs_name
        self.single_outputs = single_outputs
        self.multi_outputs_name = multi_outputs_name
        self.multi_outputs = multi_outputs

    def __repr__(self):
        return "{}({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})".format(
            self.__class__.__name__,
            self.tr_code,
            self.name,
            self.tr_name,
            self.tr_names_svr,
            self.tr_type,
            self.gfid,
            self.inputs,
            self.single_outputs_name,
            self.single_outputs,
            self.multi_outputs_name,
            self.multi_outputs,
        )

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                self.tr_code == other.tr_code
                and self.name == other.name
                and self.tr_name == other.tr_name
                and self.tr_names_svr == other.tr_names_svr
                and self.tr_type == other.tr_type
                and self.gfid == other.gfid
                and self.inputs == other.inputs
                and self.single_outputs_name == other.single_outputs_name
                and self.single_outputs == other.single_outputs
                and self.multi_outputs_name == other.multi_outputs_name
                and self.multi_outputs == other.multi_outputs
            )
        return False

    def to_dict(self):
        dic = dict(self.__dict__)
        for attr in dic:
            if isinstance(dic[attr], list):
                dic[attr] = [field.to_dict() for field in dic[attr]]
        return dic

    @classmethod
    def from_dict(cls, dic):
        output = cls()
        for name in output.__dict__:
            value = dic.get(name)
            if isinstance(value, list):
                fields = [cls.Field.from_dict(d) for d in value]
                setattr(output, name, fields)
            else:
                setattr(output, name, value)
        return output

    def get_input_names(self):
        return [input_.name for input_ in self.inputs]

    def get_single_output_names(self):
        return [output.name for output in self.single_outputs]

    def get_multi_output_names(self):
        return [output.name for output in self.multi_outputs]

    @classmethod
    def get_trinfo_by_code(cls, trcode):
        return cls._TRINFO_BY_CODE.get(trcode.lower())

    @classmethod
    def from_encfile(cls, f, tr_code=None):
        with contextlib.ExitStack() as stack:
            if isinstance(f, str):
                tr_code = os.path.splitext(f.lower())[0]
                f = stack.enter_context(open(f))
            elif tr_code is None:
                raise ValueError("Argument tr_code should be given.")

            lines = iter(f)
            lines = map(lambda line: line.rstrip("\n"), lines)
            lines = filter(lambda line: len(line.strip()) > 0, lines)

            single_outputs_name = ""
            single_outputs = []
            multi_outputs_name = ""
            multi_outputs = []

            tr_names_svr = ""
            gfid = ""

            line = next(lines)
            assert line == "[TRINFO]"
            line = next(lines)
            assert line.startswith("TRName=")
            tr_name = line.split("=", 2)[1]
            line = next(lines)
            if line.startswith("TRNameSVR="):
                tr_names_svr = line.split("=", 2)[1]
                line = next(lines)
            assert line.startswith("TRType=")
            tr_type = line.split("=", 2)[1]
            line = next(lines)
            if line.startswith("GFID="):
                gfid = line.split("=", 2)[1]
                line = next(lines)
            assert line == "[INPUT]"
            line = next(lines)
            assert line.startswith("@START_")
            tr_name_readable = line.split("_", 2)[1].split("=", 2)[0]
            line = next(lines)
            inputs = []
            while not line.startswith("@END_"):
                input_name, triple = [
                    item.strip() for item in line.strip().split("=", 2)
                ]
                triple = [item.strip() for item in triple.split(",")]
                start, offset, fid = [int(item) for item in triple]
                inputs.append(cls.Field(input_name, start, offset, fid))
                line = next(lines)
            line = next(lines)
            assert line == "[OUTPUT]"
            line = next(lines)
            assert line.startswith("@START_")
            single_outputs_name = line.split("_", 2)[1].split("=", 2)[0]
            line = next(lines)
            while not line.startswith("@END_"):
                output_name, triple = [
                    item.strip() for item in line.strip().split("=", 2)
                ]
                triple = [item.strip() for item in triple.split(",")]
                start, offset, fid = [int(item) if item else 0 for item in triple]
                single_outputs.append(cls.Field(output_name, start, offset, fid))
                line = next(lines)
            try:
                line = next(lines)
            except StopIteration:
                pass
            else:
                if line.startswith("@START_"):
                    multi_outputs_name = line.split("_", 2)[1].split("=", 2)[0]
                    line = next(lines)
                    while not line.startswith("@END_"):
                        output_name, triple = [
                            item.strip() for item in line.strip().split("=", 2)
                        ]
                        triple = [item.strip() for item in triple.split(",")]
                        start, offset, fid = [
                            int(item) if item else 0 for item in triple
                        ]
                        multi_outputs.append(cls.Field(output_name, start, offset, fid))
                        line = next(lines)
            return cls(
                tr_code,
                tr_name_readable,
                tr_name,
                tr_names_svr,
                tr_type,
                gfid,
                inputs,
                single_outputs_name,
                single_outputs,
                multi_outputs_name,
                multi_outputs,
            )

    @classmethod
    def infos_from_data_dir(cls, data_dir=None, encoding=None, module_path=None):
        if data_dir is None:
            if module_path is None:
                from koapy.backend.kiwoom_open_api_plus.utils.module_path import (
                    GetAPIModulePath,
                )

                module_path = GetAPIModulePath()
            data_dir = os.path.join(module_path, "data")
        if encoding is None:
            encoding = "euc-kr"
        cls.logger.debug("Reading files under %s", data_dir)
        enc_filenames = [filename.lower() for filename in os.listdir(data_dir)]
        enc_filenames = [
            filename
            for filename in enc_filenames
            if filename.startswith("o") and filename.endswith(".enc")
        ]
        results = []
        for filename in enc_filenames:
            full_filename = os.path.join(data_dir, filename)
            with zipfile.ZipFile(full_filename) as z:
                for info in z.infolist():
                    inner_filename = info.filename
                    tr_code = os.path.splitext(inner_filename.lower())[0]
                    cls.logger.debug(
                        "Reading file %s inside %s", inner_filename, full_filename
                    )
                    with z.open(info) as b:
                        with io.TextIOWrapper(b, encoding=encoding) as f:
                            results.append(cls.from_encfile(f, tr_code))
        return results

    _SINGLE_TO_MULTI_TRCODES = [
        "opt10072",
        "opt10073",
        "opt10075",
        "opt10076",
        "opt10085",
        "optkwfid",
        "optkwinv",
        "optkwpro",
    ]

    @classmethod
    def _single_outputs_are_actually_multi_outputs(cls, item):
        multi_outputs_name = item.multi_outputs_name
        multi_outputs = item.multi_outputs
        item.multi_outputs_name = item.single_outputs_name
        item.multi_outputs = item.single_outputs
        item.single_outputs_name = multi_outputs_name
        item.single_outputs = multi_outputs
        return item

    @classmethod
    def trinfo_by_code_from_data_dir(cls, data_dir=None, post_process=True):
        infos = cls.infos_from_data_dir(data_dir)
        result = {info.tr_code: info for info in infos}
        if post_process:
            for tr_code in result:
                if tr_code in cls._SINGLE_TO_MULTI_TRCODES:
                    item = result[tr_code]
                    item = cls._single_outputs_are_actually_multi_outputs(item)
                    result[tr_code] = item
        return result

    @classmethod
    def dump_trinfo_by_code(cls, dump_file=None, data_dir=None):
        if dump_file is None:
            dump_file = cls._TRINFO_BY_CODE_DUMP_FILEPATH
        with contextlib.ExitStack() as stack:
            if isinstance(dump_file, str):
                dump_filename = dump_file
                dump_file = stack.enter_context(open(dump_file, "w", encoding="utf-8"))
            else:
                dump_filename = None
            result = cls.trinfo_by_code_from_data_dir(data_dir)
            for tr_code in result:
                result[tr_code] = result[tr_code].to_dict()
            if dump_filename is not None:
                cls.logger.debug("Saving trinfo to %s", dump_filename)
            return json.dump(
                result,
                dump_file,
                indent=4,
                sort_keys=True,
                ensure_ascii=False,
            )

    @classmethod
    def trinfo_by_code_from_dump_file(cls, dump_file=None):
        if dump_file is None:
            dump_file = cls._TRINFO_BY_CODE_DUMP_FILEPATH
        with contextlib.ExitStack() as stack:
            if isinstance(dump_file, str):
                if os.path.exists(dump_file) and os.path.getsize(dump_file) > 0:
                    dump_file = stack.enter_context(
                        open(dump_file, "r", encoding="utf-8")
                    )
                else:
                    return {}
            result = json.load(dump_file)
        for tr_code in result:
            item = cls.from_dict(result[tr_code])
            result[tr_code] = item
        return result

    @classmethod
    def load_from_dump_file(cls, dump_file=None):
        cls._TRINFO_BY_CODE = cls.trinfo_by_code_from_dump_file(dump_file)

    @classmethod
    def load_from_data_dir(cls, data_dir=None):
        cls._TRINFO_BY_CODE = cls.trinfo_by_code_from_data_dir(data_dir)

    @classmethod
    def load(cls):
        try:
            cls.load_from_data_dir()
        except FileNotFoundError:
            cls.load_from_dump_file()


KiwoomOpenApiPlusTrInfo.Field.__outer_class__ = KiwoomOpenApiPlusTrInfo
KiwoomOpenApiPlusTrInfo.load()


def main():
    KiwoomOpenApiPlusTrInfo.dump_trinfo_by_code()


def infer_fids_by_tr_outputs(output_filename=None):
    if output_filename is None:
        output_filename = "fid.xlsx"
    infos = KiwoomOpenApiPlusTrInfo.infos_from_data_dir()
    fields = []
    for info in infos:
        for field in info.single_outputs:
            fields.append(field)
        for field in info.multi_outputs:
            fields.append(field)
    pairs = [[field.fid, field.name] for field in fields if field.fid != -1]
    import string  # pylint: disable=import-outside-toplevel

    for pair in pairs:
        if pair[1].startswith("풋_"):
            pair[1] = pair[1][2:]
        if not pair[1][0] in string.ascii_letters and pair[1][-1] in "ns":
            pair[1] = pair[1][:-1]
        pair[1] = pair[1].upper()
    pairs = [tuple(pair) for pair in pairs]
    pairs = list(set(pairs))
    pairs = sorted(pairs, key=lambda item: item[0])
    import pandas as pd  # pylint: disable=import-outside-toplevel

    df = pd.DataFrame.from_records(pairs)
    df.to_excel(output_filename, header=False, index=False)


if __name__ == "__main__":
    main()
