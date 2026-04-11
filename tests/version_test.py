import pathlib
import re
import siepic_forge as siepic


def test_version():
    assert siepic.__version__ == siepic.ebeam_si().version
    assert siepic.__version__ == siepic.ebeam_sin().version
    pyproject = pathlib.Path("pyproject.toml")
    if pyproject.is_file():
        contents = pyproject.read_text()
        match = re.search('version = "([^"]*)"', contents)
        assert match and match.groups(1)[0] == siepic.__version__
