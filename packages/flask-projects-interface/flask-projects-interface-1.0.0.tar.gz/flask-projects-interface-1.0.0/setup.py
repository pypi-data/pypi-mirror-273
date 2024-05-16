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
VERSION = '1.0.0'
DESCRIPTION = "flask projects系列的接口集"
LONG_DESCRIPTION = '一个涵盖了flask projects自定义扩展所需所有指定抽象基类的第三方包合集，用于在脱离flask projects系列core包的情况下，仍能够进行扩展编写'

setup(
    name="flask-projects-interface",

    author="bichuantao",
    author_email='17826066203@163.com',

    keywords=['python', 'flask', 'interface', 'Rapid development'],
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ababbabbb/flask_project_interface',
    license='MIT',

    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[]
)
