import json

class JsonSerializable:

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
