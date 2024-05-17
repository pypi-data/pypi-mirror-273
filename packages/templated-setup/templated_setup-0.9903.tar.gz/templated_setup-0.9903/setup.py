import os
from setuptools import setup

DESCRIPTION = "A quick and easy replacement for some `setup.py` implementations."

def __init_description(readme_file_path_) -> "str":
	description = None
	if not os.path.exists(readme_file_path_):
		raise FileNotFoundError(f"No such file or directory: [{readme_file_path_}].")
	if not os.path.isabs(readme_file_path_):
		readme_file_path_ = os.path.abspath(readme_file_path_)
	if not os.path.isfile(readme_file_path_):
		raise FileNotFoundError(f"Expected [{readme_file_path_}] to be a file. Found a directory instead.")
	with open(readme_file_path_, "r") as f:
		description = f.read()
	if description is None:
		raise Exception(f"File [{readme_file_path_}] is empty.")
	return description


version_number = "0.9903"
notes = "No notes."

long_description = __init_description("README.md")
long_description += f"\n## V{version_number}\n"
long_description += notes

setup(
	name="templated_setup",
	version=version_number,
	author="matrikater (Joel Watson)",
	description=DESCRIPTION,
	author_email="administraitor@matriko.xyz",
	install_requires=[
		"setuptools",
		"twine"
	],
	long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
	long_description=long_description,
)