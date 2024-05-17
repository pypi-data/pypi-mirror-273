from um2dpi import um2dpi, dpi2um


def test_um2dpi():
    assert int(um2dpi(10)) == 2540
    assert int(um2dpi(20)) == 1270


def test_dpi2um():
    assert int(dpi2um(2540)) == 10
    assert int(dpi2um(1270)) == 20
