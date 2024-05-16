import stldim
def test_plain():
    print(dir(stldim))
    assert stldim.sanitize_filename("test.stl") == "test_stl"

def test_spaces():
    assert stldim.sanitize_filename("test test.stl") == "test_test_stl"

def test_special_chars():
    assert stldim.sanitize_filename("test!@#$%^&*().stl") == "test___________stl"

def test_leading_numbers():
    assert stldim.sanitize_filename("11test.stl") == "__test_stl"

def test_trailing_numbers():
    assert stldim.sanitize_filename("test11.stl") == "test11_stl"

def test_no_extension():
    assert stldim.sanitize_filename("test") == "test"

def test_subdirectory():
    assert stldim.sanitize_filename("subdir/test.stl") == "test_stl"