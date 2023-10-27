# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join as path_join
from setuptools import find_packages, setup

CURDIR = abspath(dirname(__file__))
SRC = path_join(CURDIR, 'src')

with open(path_join(SRC, 'oxygen', 'version.py')) as f:
    exec(f.read())

KEYWORDS = ('robotframework testing testautomation acceptancetesting atdd bdd'
            'reporting testreporting')

SHORT_DESC = ('Oxygen is an extensible tool for Robot Framework that '
              'enables you to integrate running other testing tools and their '
              'reports as part of Robot Framework\'s reporting.')

with open(path_join(CURDIR, 'README.md'), 'r') as readme:
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
           'junitparser==2.0',
           'PyYAML>=3.13',
           'pydantic>=2.4.2'
      ],
      packages=find_packages(SRC),
      package_dir={'': 'src'},
      package_data={'oxygen': ['*.yml']},
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS,
      version=VERSION,
      description=SHORT_DESC,
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown")
