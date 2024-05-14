import setuptools
from pathlib import Path

long_description = Path("README.md").read_text()
setuptools.setup(
    name="holamundoplayer_sv_test",
    version="0.0.1",
    long_description=long_description,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    ),
)
