import contextlib

from os import PathLike
from pathlib import Path
from typing import Optional, Sequence, TextIO, Union


class KiwoomOpenApiPlusConditionEntry:
    def __init__(
        self,
        header,
        item_id,
        group_id,
        group_name,
        group_tp,
        name,
        group_id_small,
        order_no,
        type_position,
        upjong,
        portfolio,
        recommend,
        acc,
        group,
        excepts,
        month,
        exp,
        count,
        rules,
    ):
        self.header = header
        self.item_id = item_id
        self.group_id = group_id
        self.group_name = group_name
        self.group_tp = group_tp
        self.name = name
        self.group_id_small = group_id_small
        self.order_no = order_no
        self.type_position = type_position
        self.upjong = upjong
        self.portfolio = portfolio
        self.recommend = recommend
        self.acc = acc
        self.group = group
        self.excepts = excepts
        self.month = month
        self.exp = exp
        self.count = count
        self.rules = rules

    def __repr__(self):
        template = "{}" + "({})".format(", ".join(["{!r}" for _ in range(19)]))
        return template.format(
            self.__class__.__name__,
            self.header,
            self.item_id,
            self.group_id,
            self.group_name,
            self.group_tp,
            self.name,
            self.group_id_small,
            self.order_no,
            self.type_position,
            self.upjong,
            self.portfolio,
            self.recommend,
            self.acc,
            self.group,
            self.excepts,
            self.month,
            self.exp,
            self.count,
            self.rules,
        )

    @classmethod
    def from_datfile(cls, f: TextIO):
        lines = iter(f)
        lines = map(lambda line: line.rstrip("\n"), lines)
        line = next(lines)
        while line == "":
            line = next(lines)
        assert line.startswith("[") and line.endswith("]")
        header = line
        line = next(lines)
        assert line.startswith("ItemID=")
        item_id = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("GroupID=")
        group_id = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("GroupName=")
        group_name = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("GroupTp=")
        group_tp = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Name=")
        name = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("GroupId=")
        group_id_small = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("OrderNo=")
        order_no = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("TypePosition=")
        type_position = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Upjong=")
        upjong = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Portfolio=")
        portfolio = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Recommend=")
        recommend = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Acc=")
        acc = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Group=")
        group = line.split("=", 2)[1]
        excepts = []
        for i in range(22):
            line = next(lines)
            assert line.startswith(f"Except{i+1}=")
            except_item = line.split("=", 2)[1]
            excepts.append(except_item)
        line = next(lines)
        assert line.startswith("Month=")
        month = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Exp=")
        exp = line.split("=", 2)[1]
        line = next(lines)
        assert line.startswith("Count=")
        count = line.split("=", 2)[1]
        count = int(count)
        rules = []
        for i in range(count):
            line = next(lines)
            assert line.startswith(f"{str(i).zfill(2)}=")
            rule_num, rule_expr = line.split("=", 2)
            rule = (rule_num, rule_expr)
            rules.append(rule)
        return cls(
            header,
            item_id,
            group_id,
            group_name,
            group_tp,
            name,
            group_id_small,
            order_no,
            type_position,
            upjong,
            portfolio,
            recommend,
            acc,
            group,
            excepts,
            month,
            exp,
            count,
            rules,
        )


class KiwoomOpenApiPlusConditionFile:
    def __init__(
        self, version: str, entries: Sequence[KiwoomOpenApiPlusConditionEntry]
    ):
        self.version = version
        self.entries = list(entries)

    def __repr__(self):
        template = "{}" + "({})".format(", ".join(["{!r}" for _ in range(2)]))
        return template.format(
            self.__class__.__name__,
            self.version,
            self.entries,
        )

    @classmethod
    def from_datfile(
        cls, f: Union[str, PathLike, TextIO], encoding: Optional[str] = None
    ):
        if isinstance(f, str):
            f = Path(f)
        if encoding is None:
            encoding = "euc-kr"
        with contextlib.ExitStack() as stack:
            if isinstance(f, PathLike):
                f = open(f, "r", encoding=encoding)
                f = stack.enter_context(f)
            lines = iter(f)
            lines = map(lambda line: line.rstrip("\n"), lines)
            line = next(lines)
            assert line == "[Version]"
            line = next(lines)
            assert line.startswith("ver=")
            version = line.split("=", 2)[1]
            entries = []
            should_stop = False
            while not should_stop:
                try:
                    cond = KiwoomOpenApiPlusConditionEntry.from_datfile(f)
                except StopIteration:
                    break
                else:
                    entries.append(cond)
            return cls(version, entries)
