# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join as path_join
from setuptools import find_packages, setup

CURDIR = abspath(dirname(__file__))
SRC = path_join(CURDIR, 'src')

# get VERSION number
with open(path_join(SRC, 'oxygen', 'version.py')) as f:
    exec(f.read())

KEYWORDS = ('')

SHORT_DESC = ('')

with open(path_join(CURDIR, 'README'), 'r') as readme:
    LONG_DESCRIPTION = readme.read()

CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
Programming Language :: Python :: 3 :: Only
Operating System :: OS Independent
Topic :: Software Development :: Testing
License :: OSI Approved :: MIT License
'''.strip().splitlines()

setup(name='robotframework-oxygen',
      author='Eficode Oy',
      author_email='info@eficode.com',
      url='',
      license='MIT',
      install_requires=[
           'robotframework>=3.0.4',
           'junitparser>=1.2.2',
           'PyYAML>=3.13'
      ],
      packages=find_packages(SRC),
      package_dir={'': 'src'},
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS,
      version=VERSION,
      description=SHORT_DESC,
      long_description=LONG_DESCRIPTION)
