import um2dpi


def test_cli(capsys, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr("sys.argv", ["um2dpi", "10"])
        um2dpi.cli()
        captured = capsys.readouterr()
        assert captured.out == "10.0 μm: 2540.00 dpi\n"

        m.setattr("sys.argv", ["um2dpi", "-r", "2540"])
        um2dpi.cli()
        captured = capsys.readouterr()
        assert captured.out == "2540.0 dpi: 10.00 μm\n"
