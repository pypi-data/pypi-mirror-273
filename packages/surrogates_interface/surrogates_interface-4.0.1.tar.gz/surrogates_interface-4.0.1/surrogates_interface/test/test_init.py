try:
    import tomllib  # From Python 3.11.
except ModuleNotFoundError:
    import tomli as tomllib  # Before Python 3.11.

import surrogates_interface


def test_version():
    with open("pyproject.toml", "rb") as fid:
        data = tomllib.load(fid)
    assert surrogates_interface.__version__ == data["tool"]["poetry"]["version"]
