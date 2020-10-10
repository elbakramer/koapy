
import pytest

from koapy.utils.collections import ChainList

def test_chainlist_getitem():
    d1 = [1,2,3]
    d2 = [4,5,6]
    d3 = [7,8,9]
    c = ChainList([d1, d2, d3])
    d = [1,2,3,4,5,6,7,8,9]
    dlen = len(d)
    for i in range(dlen):
        assert c[i] == d[i]
        assert c[-1-i] == d[-1-i]
    with pytest.raises(IndexError):
        assert c[dlen] == d[dlen]
    with pytest.raises(IndexError):
        assert c[-dlen-1] == d[-dlen-1]
    cc = ChainList([c, c, c])
    dd = ChainList([d, d, d])
    ddlen = len(dd)
    for i in range(ddlen):
        assert cc[i] == dd[i]
        assert cc[-1-i] == dd[-1-i]
    with pytest.raises(IndexError):
        assert cc[ddlen] == dd[ddlen]
    with pytest.raises(IndexError):
        assert cc[-ddlen-1] == dd[-ddlen-1]

def test_chainlist_slice():
    a = [1,2,3]
    b = [4,5,6]
    c = ChainList([a, b])
    d = [1,2,3,4,5,6]
    assert c[0:1] == d[0:1]
    assert c[0:3] == d[0:3]
    assert c[0:6] == d[0:6]
    assert c[0:6:2] == d[0:6:2]
    assert c[1:6:2] == d[1:6:2]
    assert c[:4] == d[:4]
    assert c[2:] == d[2:]
    assert c[::-1] == d[::-1]
    assert c[-1:-6] == d[-1:-6]
    assert c[-1:-6:-1] == d[-1:-6:-1]
    assert c[-1:-6:-2] == d[-1:-6:-2]
    assert c[1:-1] == d[1:-1]
    assert c[1:-1:-1] == d[1:-1:-1]
    assert c[-1:1] == d[-1:1]
    with pytest.raises(ValueError):
        assert c[0:6:0] == d[0:6:0]

def test_chainlist_mutation():
    a = [1,2]
    b = [4,5,6]
    c = ChainList([a, b])
    a.append(3)
    d = [1,2,3,4,5,6]

    assert c[0] == d[0]
    assert c[1] == d[1]
    assert c[2] == d[2]
    assert c[3] == d[3]
    assert c[4] == d[4]
    assert c[5] == d[5]
    assert c[-1] == d[-1]
    assert c[-2] == d[-2]
    assert c[-3] == d[-3]
    assert c[-4] == d[-4]
    assert c[-5] == d[-5]
    assert c[-6] == d[-6]
    with pytest.raises(IndexError):
        assert c[6] == d[6]
    with pytest.raises(IndexError):
        assert c[-7] == d[-7]

    assert c[0:1] == d[0:1]
    assert c[0:3] == d[0:3]
    assert c[0:6] == d[0:6]
    assert c[0:6:2] == d[0:6:2]
    assert c[1:6:2] == d[1:6:2]
    assert c[:4] == d[:4]
    assert c[2:] == d[2:]
    assert c[::-1] == d[::-1]
    assert c[-1:-6] == d[-1:-6]
    assert c[-1:-6:-1] == d[-1:-6:-1]
    assert c[-1:-6:-2] == d[-1:-6:-2]
    assert c[1:-1] == d[1:-1]
    assert c[1:-1:-1] == d[1:-1:-1]
    assert c[-1:1] == d[-1:1]
    with pytest.raises(ValueError):
        assert c[0:6:0] == d[0:6:0]

def test_chainlist_iter():
    d1 = [1,2,3]
    d2 = [4,5,6]
    d3 = [7,8,9]
    c = ChainList([d1, d2, d3])
    d = [1,2,3,4,5,6,7,8,9]
    clen = 0
    dlen = len(d)
    for i, ci in enumerate(c):
        assert ci == d[i]
        clen += 1
    assert clen == dlen
    cc = ChainList([c, c, c])
    dd = ChainList([d, d, d])
    cclen = 0
    ddlen = len(dd)
    for i, cci in enumerate(cc):
        assert cci == dd[i]
        cclen += 1
    assert cclen == ddlen

def test_chainlist_with_emtpy():
    d1 = [1,2,3]
    d2 = []
    d3 = [7,8,9]
    c = ChainList([d1, d2, d3])
    d = [1,2,3,7,8,9]
    dlen = len(d)
    for i in range(dlen):
        assert c[i] == d[i]
        assert c[-1-i] == d[-1-i]
    with pytest.raises(IndexError):
        assert c[dlen] == d[dlen]
    with pytest.raises(IndexError):
        assert c[-dlen-1] == d[-dlen-1]
    cc = ChainList([c, c, c])
    dd = ChainList([d, d, d])
    ddlen = len(dd)
    for i in range(ddlen):
        assert cc[i] == dd[i]
        assert cc[-1-i] == dd[-1-i]
    with pytest.raises(IndexError):
        assert cc[ddlen] == dd[ddlen]
    with pytest.raises(IndexError):
        assert cc[-ddlen-1] == dd[-ddlen-1]
