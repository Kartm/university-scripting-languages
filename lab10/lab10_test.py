import pytest

from lab10 import app10


def test_reqstr2obj_argument():
    with pytest.raises(TypeError):
        app10.reqstr2obj(123)

    with pytest.raises(TypeError):
        app10.reqstr2obj([])