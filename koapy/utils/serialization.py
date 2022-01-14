import io
import json
import os


class JsonSerializable:
    def to_dict(self):
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, dic):
        output = cls()
        for name in output.__dict__:
            setattr(output, name, dic.get(name))
        return output

    def to_json(self, f=None, encoding=None):
        if f is None:
            return json.dumps(self.to_dict())
        elif isinstance(f, str):
            with open(f, "w", encoding=encoding) as f:
                return json.dump(self.to_dict(), f)
        elif isinstance(f, io.TextIOBase):
            return json.dump(self.to_dict(), f)
        else:
            raise ValueError("Unsupported argument type: %s" % type(f))

    @classmethod
    def from_json(cls, jsn, encoding=None):
        if isinstance(jsn, str):
            if jsn.startswith("{") and jsn.endswith("}"):
                dic = json.loads(jsn)
            elif os.path.exists(jsn):
                with open(jsn, "r", encoding=encoding) as f:
                    dic = json.load(f)
            else:
                dic = json.loads(jsn)
        elif isinstance(jsn, io.TextIOBase):
            dic = json.load(jsn)
        else:
            raise ValueError("Unsupported argument type: %s" % type(jsn))
        return cls.from_dict(dic)
