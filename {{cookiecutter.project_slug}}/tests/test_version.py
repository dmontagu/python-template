from pathlib import Path

import toml

import {{cookiecutter.project_slug}}


def test_version():
    version = {{cookiecutter.project_slug}}.__version__
    pyproject_toml = Path({{cookiecutter.project_slug}}.__file__).parent.parent / "pyproject.toml"
    contents = pyproject_toml.read_text()
    assert toml.loads(contents)["tool"]["poetry"]["version"] == version
