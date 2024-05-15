import stldim
from stl import mesh
import pytest

def test_3dbenchy():
    main_body = mesh.Mesh.from_file("tests/3DBenchy.stl")
    
    minx, maxx, miny, maxy, minz, maxz = stldim.find_mins_maxs(main_body)
    
    assert pytest.approx(minx) == -29.176
    assert pytest.approx(maxx) == 30.825
    assert pytest.approx(miny) == -15.502
    assert pytest.approx(maxy) == 15.502
    assert pytest.approx(minz) == 0.0
    assert pytest.approx(maxz) == 48.0
