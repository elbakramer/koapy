import os
import io
import json
import zipfile
import contextlib


class TrInfo:

    _TRINFO_BY_CODE_DUMP_FILENAME = 'trinfo_by_code.json'
    _TRINFO_BY_CODE = {}

    class Field:

        __outer_class__ = None

        def __init__(self, name=None, start=None, offset=None, fid=None):
            self.name = name
            self.start = start
            self.offset = offset
            self.fid = fid

        def __repr__(self):
            return '%s.%s(%r, %r, %r, %r)' % (
                self.__outer_class__.__name__,
                self.__class__.__name__,
                self.name,
                self.start,
                self.offset,
                self.fid)

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
        def from_json(cls, jsn):
            if isinstance(jsn, str):
                dic = json.loads(jsn)
            elif isinstance(jsn, io.TextIOBase):
                dic = json.load(jsn)
            else:
                raise ValueError()
            return cls.from_dict(dic)

    def __init__(self, tr_code=None, name=None, tr_name=None, tr_names_svr=None, tr_type=None, gfid=None,
                 inputs=None, single_outputs_name=None, single_outputs=None, multi_outputs_name=None, multi_outputs=None):
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
        return '%s(%r, %r, %r, %r, %r, %r, %r, %r, %r, %r)' % (
            self.__class__.__name__,
            self.name,
            self.tr_name,
            self.tr_names_svr,
            self.tr_type,
            self.gfid,
            self.inputs,
            self.single_outputs_name,
            self.single_outputs,
            self.multi_outputs_name,
            self.multi_outputs
        )

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

    def to_json(self, filename=None):
        if filename is None:
            return json.dumps(self.to_dict())
        else:
            with open(filename, 'w') as f:
                return json.dump(self.to_dict(), f)

    @classmethod
    def from_json(cls, jsn):
        if isinstance(jsn, str):
            dic = json.loads(jsn)
        elif isinstance(jsn, io.TextIOBase):
            dic = json.load(jsn)
        else:
            raise ValueError()
        return cls.from_dict(dic)

    def get_input_names(self):
        return [input_.name for input_ in self.inputs]

    def get_single_output_names(self):
        return [output.name for output in self.single_outputs]

    def get_multi_output_names(self):
        return [output.name for output in self.multi_outputs]

    @classmethod
    def get_trinfo_by_code(cls, trcode):
        return cls._TRINFO_BY_CODE.get(trcode)

    @classmethod
    def from_encfile(cls, f, tr_code=''):
        with contextlib.ExitStack() as stack:
            if isinstance(f, str):
                tr_code = os.path.splitext(f.lower())[0]
                f = stack.enter_context(open(f))

            lines = iter(f)
            lines = map(lambda line: line.rstrip('\n'), lines)
            lines = filter(lambda line: len(line.strip()) > 0, lines)

            single_outputs_name = ''
            single_outputs = []
            multi_outputs_name = ''
            multi_outputs = []

            tr_names_svr = ''
            gfid = ''

            line = next(lines)
            assert line == '[TRINFO]'
            line = next(lines)
            assert line.startswith('TRName=')
            tr_name = line.split('=', 2)[1]
            line = next(lines)
            if line.startswith('TRNameSVR='):
                tr_names_svr = line.split('=', 2)[1]
                line = next(lines)
            assert line.startswith('TRType=')
            tr_type = line.split('=', 2)[1]
            line = next(lines)
            if line.startswith('GFID='):
                gfid = line.split('=', 2)[1]
                line = next(lines)
            assert line == '[INPUT]'
            line = next(lines)
            assert line.startswith('@START_')
            tr_name_readable = line.split('_', 2)[1].split('=', 2)[0]
            line = next(lines)
            inputs = []
            while not line.startswith('@END_'):
                input_name, triple = [item.strip() for item in line.strip().split('=', 2)]
                triple = [item.strip() for item in triple.split(',')]
                start, offset, fid = [int(item) for item in triple]
                inputs.append(cls.Field(input_name, start, offset, fid))
                line = next(lines)
            line = next(lines)
            assert line == '[OUTPUT]'
            line = next(lines)
            assert line.startswith('@START_')
            single_outputs_name = line.split('_', 2)[1].split('=', 2)[0]
            line = next(lines)
            while not line.startswith('@END_'):
                output_name, triple = [item.strip() for item in line.strip().split('=', 2)]
                triple = [item.strip() for item in triple.split(',')]
                start, offset, fid = [int(item) if item else 0 for item in triple]
                single_outputs.append(cls.Field(output_name, start, offset, fid))
                line = next(lines)
            try:
                line = next(lines)
            except StopIteration:
                pass
            else:
                if line.startswith('@START_'):
                    multi_outputs_name = line.split('_', 2)[1].split('=', 2)[0]
                    line = next(lines)
                    while not line.startswith('@END_'):
                        output_name, triple = [item.strip() for item in line.strip().split('=', 2)]
                        triple = [item.strip() for item in triple.split(',')]
                        start, offset, fid = [int(item) if item else 0 for item in triple]
                        multi_outputs.append(cls.Field(output_name, start, offset, fid))
                        line = next(lines)
            return cls(tr_code, tr_name_readable, tr_name, tr_names_svr, tr_type, gfid,
                       inputs, single_outputs_name, single_outputs, multi_outputs_name, multi_outputs)

    @classmethod
    def infos_from_data_dir(cls, data_dir=None, encoding='euc-kr'):
        if data_dir is None:
            data_dir = r'C:\OpenAPI\data'
        enc_filenames = [filename.lower() for filename in os.listdir(data_dir)]
        enc_filenames = [filename for filename in enc_filenames if filename.startswith('o') and filename.endswith('.enc')]
        results = []
        for filename in enc_filenames:
            with zipfile.ZipFile(os.path.join(data_dir, filename)) as z:
                for info in z.infolist():
                    inner_filename = info.filename
                    tr_code = os.path.splitext(inner_filename.lower())[0]
                    with z.open(info) as b:
                        with io.TextIOWrapper(b, encoding=encoding) as f:
                            results.append(cls.from_encfile(f, tr_code))
        return results

    @classmethod
    def trinfo_by_name_from_data_dir(cls, data_dir=None):
        infos = cls.infos_from_data_dir(data_dir)
        result = {info.tr_code:info for info in infos}
        return result

    @classmethod
    def dump_trinfo_by_name(cls, dump_file=None):
        with contextlib.ExitStack() as stack:
            if dump_file is None:
                dump_file = os.path.join(os.path.dirname(__file__), 'data', cls._TRINFO_BY_CODE_DUMP_FILENAME)
            if isinstance(dump_file, str):
                dump_file = stack.enter_context(open(dump_file, 'w'))
            result = cls.trinfo_by_name_from_data_dir()
            for tr_code in result:
                result[tr_code] = result[tr_code].to_dict()
            return json.dump(result, dump_file)

    @classmethod
    def trinfo_by_name_from_dump_file(cls, dump_file=None):
        with contextlib.ExitStack() as stack:
            if dump_file is None:
                dump_file = os.path.join(os.path.dirname(__file__), 'data', cls._TRINFO_BY_CODE_DUMP_FILENAME)
            if isinstance(dump_file, str) and os.path.exists(dump_file):
                dump_file = stack.enter_context(open(dump_file, 'r'))
                result = json.load(dump_file)
                for tr_code in result:
                    result[tr_code] = cls.from_dict(result[tr_code])
                return result
        return {}


TrInfo.Field.__outer_class__ = TrInfo
TrInfo._TRINFO_BY_CODE = TrInfo.trinfo_by_name_from_dump_file()


def main():
    TrInfo.dump_trinfo_by_name()

def infer_fids_by_tr_outputs():
    infos = TrInfo.infos_from_data_dir()
    fields = []
    for info in infos:
        for field in info.single_outputs:
            fields.append(field)
        for field in info.multi_outputs:
            fields.append(field)
    pairs = [[field.fid, field.name] for field in fields if field.fid != -1]
    import string # pylint: disable=import-outside-toplevel
    for pair in pairs:
        if pair[1].startswith('풋_'):
            pair[1] = pair[1][2:]
        if not pair[1][0] in string.ascii_letters and pair[1][-1] in 'ns':
            pair[1] = pair[1][:-1]
        pair[1] = pair[1].upper()
    pairs = [tuple(pair) for pair in pairs]
    pairs = list(set(pairs))
    pairs = sorted(pairs, key=lambda item: item[0])
    import pandas as pd # pylint: disable=import-outside-toplevel
    df = pd.DataFrame.from_records(pairs)
    df.to_excel('fid.xlsx', header=False, index=False)


if __name__ == '__main__':
    main()
