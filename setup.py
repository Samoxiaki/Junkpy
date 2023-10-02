import setuptools
from pathlib import Path

setuptools.setup(
	name = "junkpy",
	version = "0.4.1",
	author = "Samoxiaki",
	author_email = "samoxiaki@yahoo.com",
	url = "https://github.com/Samoxiaki/Junkpy",
	description = "Library for processing Junk configuration files",
	long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
	packages = ["junkpy"],
	install_requires = ["lark"]
)
