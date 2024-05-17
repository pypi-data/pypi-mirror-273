from setuptools import setup, find_packages

# Read version from the VERSION file
with open('REMLA_Test_Lib_version/VERSION', 'r') as version_file:
    version = version_file.read().strip()

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    # long_description = "\\n" + fh.read()
    long_description = fh.read()

setup(
name='REMLA-Test-Lib-version',
version=version,
author='Nick Dubbeldam',
author_email='nick.dubbeldasm@live.nl',
description='A version-aware library designed to provide robust version management and utility functions',
long_description_content_type="text/markdown",
long_description=long_description,
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
package_data={'': ['VERSION']},
include_package_data=True,
)