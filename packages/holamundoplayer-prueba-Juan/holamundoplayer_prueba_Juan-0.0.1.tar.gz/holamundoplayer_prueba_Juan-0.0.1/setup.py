import setuptools
from pathlib import Path

setuptools.setup(
    name = "holamundoplayer_prueba_Juan",
    version = "0.0.1",
    long_description = Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    )

)