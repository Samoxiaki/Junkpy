import setuptools
from pathlib import Path

setuptools.setup(
	name = "junkpy",
	version = "0.3.0",
	author = "Samoxiaki",
	author_email = "samoxiaki@yahoo.com",
	url = "https://github.com/Samoxiaki/Junkpy",
	description = "Extended JSON Library for Configuration Files",
	long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
	packages = ["junkpy"],
	install_requires = ["lark"]
)
