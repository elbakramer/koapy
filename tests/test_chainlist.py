
import pytest

from koapy.utils.collections import ChainList

def test_chainlist_getitem():
    a = [1,2,3]
    b = [4,5,6]
    c = ChainList([a, b])
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
