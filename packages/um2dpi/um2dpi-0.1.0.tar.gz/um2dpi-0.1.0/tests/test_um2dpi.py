from um2dpi import um2dpi


def test_um2dpi():
    assert int(um2dpi(10)) == 2540
    assert int(um2dpi(20)) == 1270
