from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'A Simple Algorithm utils with protobuf in python'
LONG_DESCRIPTION = 'A package that include  encode/decode algo for proto witout need a .proto file'

setup(
    name="h9nt",
    version=VERSION,
    author="vardxg",
    author_email="<vardxgdev@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyproto', 'json', 'user_agent', 're'],
    keywords=['python', 'dev', 'free', 'algo'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)