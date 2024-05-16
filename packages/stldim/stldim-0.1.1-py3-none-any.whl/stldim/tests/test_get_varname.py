import stldim

def test_empty_varname():
    assert stldim.get_varname("test.stl", "") == "test_stl"

def test_none_varname():
    assert stldim.get_varname("test.stl", None) == "test_stl"

def test_varname():
    assert stldim.get_varname("test.stl", "foobar") == "foobar"