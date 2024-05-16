"""
- author:bichuantao
- creation time:2024/5/15
"""

import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.1'
DESCRIPTION = "flask projects系列快速开发手脚架核心"

setup(
    name="flask-p",

    author="bichuantao",
    author_email='17826066203@163.com',

    keywords=['python', 'flask', 'projects', 'Rapid development'],
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ababbabbb/flask_project_core',
    license='MIT',

    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'flask'
    ]
)
