#!/usr/bin/env python

import setuptools
# import sys
import re


def readme():
    with open('./README.org') as file:
        while line := file.readline():
            if match := re.search(r'^#\+title: (.*)',  line.rstrip()):
                return match.group(1)
            return "MISSING TITLE in ./README.org"

def longDescription():
    try:
        import pypandoc
    except ImportError:
        result = "warning: pypandoc module not found, could not convert to RST"
        return result
    return pypandoc.convert_file('README.org', 'rst')

####+BEGIN: b:py3:pypi/nextVersion :increment 0.01

__version__ = 0.91

####+END:

####+BEGIN: b:py3:pypi/requires :extras ("bisos.transit")

requires = [
"blee",
"blee.csPlayer",
"bisos",
"bisos.b",
"bisos.banna",
"bisos.common",
"bisos.transit",
]
####+END:

####+BEGIN: b:py3:pypi/scripts :comment ""

scripts = [
'./bin/facter.cs',
'./bin/roInv-facter.cs',
'./bin/roPerf-facter.cs',
]
####+END:


setuptools.setup(
    name='bisos.facter',
    version=__version__,
    # namespace_packages=['bisos'],
    packages=setuptools.find_packages(),
    scripts=scripts,
    requires=requires,
    include_package_data=True,
    zip_safe=False,
    author='Mohsen Banan',
    author_email='libre@mohsen.1.banan.byname.net',
    maintainer='Mohsen Banan',
    maintainer_email='libre@mohsen.1.banan.byname.net',
    url='http://www.by-star.net/PLPC/180047',
    license='AGPL',
    description=readme(),
    long_description=longDescription(),
    download_url='http://www.by-star.net/PLPC/180047',
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
