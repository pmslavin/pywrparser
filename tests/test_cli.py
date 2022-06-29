import pytest

from pywrparser import parse


def test_usage(capsys):
    """ Default action is to display usage and sys.exit """
    with pytest.raises(SystemExit) as exc:
        args = parse.configure_args([])
    assert exc.type == SystemExit
    usage = capsys.readouterr().out
    assert usage.startswith("usage") and usage.endswith("pywrparser\n")


def test_version(capsys):
    from pywrparser import __version__
    args = parse.configure_args(["--version"])
    with pytest.raises(SystemExit) as exc:
        parse.handle_args(args)
    assert exc.type == SystemExit
    version = capsys.readouterr().out
    assert version == __version__ + '\n'  # print adds newline
