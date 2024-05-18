from setuptools import find_packages, setup


def read_file(file):
	with open(file, "r") as fh:
		return fh.read()

# py -m build
# py -m twine upload dist/*


setup(
	name="dexscreener-apis",
	packages=find_packages(),
	version="0.3.1",
	license="MIT",

	description="Python wrapper for the 'dexscreener.com' API",
	long_description=read_file("README.md"),
	long_description_content_type="text/markdown",

	author="",
	author_email="",

	keywords=[
		"dexscreener",
		"crypto",
		"cryptocurrency",
		"bitcoin"
	],

	install_requires=[
		"requests",
		"pydantic",
		"certifi",
		"aiohttp"
	],

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Build Tools",
	],

	python_requires='>=3.9'
)
