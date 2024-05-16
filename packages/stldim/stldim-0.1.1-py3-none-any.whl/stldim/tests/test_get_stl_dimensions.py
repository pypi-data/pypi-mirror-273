import stldim
from stl import mesh
import pytest

def test_3dbenchy():
    stl_dimensions = stldim.get_stl_dimensions("tests/3DBenchy.stl")

    assert pytest.approx(stl_dimensions['minx']) == -29.176
    assert pytest.approx(stl_dimensions['maxx']) == 30.825
    assert pytest.approx(stl_dimensions['miny']) == -15.502
    assert pytest.approx(stl_dimensions['maxy']) == 15.502
    assert pytest.approx(stl_dimensions['minz']) == 0.0
    assert pytest.approx(stl_dimensions['maxz']) == 48.0
