"""
"""
from setuptools import setup

kw = {
	"name": "wopr",
	"version": "0.1.0",
	"description": "WOPR - War Operation Plan Response",
	"long_description": __doc__,
	"url": "https://github.com/sysr-q/wopr",
	"author": "sysr-q",
	"author_email": "chris@gibsonsec.org",
	"license": "MIT",
	"packages": [
		"wopr",
	],
	"package_dir": {
		"wopr": "wopr",
	},
	"install_requires": [
		"drawille",
	],
	"zip_safe": False,
}

if __name__ == "__main__":
	setup(**kw)
