# -*- coding: utf-8 -*-
# Copyright (c) 2011 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='pyplete',
    version='0.0.1',
    description="PYPLETE (PYthon autocomPLETE) is a interface to autocomplete in python",
    long_description=(read('README.rst') + '\n\n' + read('CHANGES')),
    keywords='pyplete, python,autocomplete,python autocomplete,python analizer',
    author='Pablo Martin',
    author_email='goinnn@gmail.com',
    url='https://github.com/goinnn/pyplete',
    license="Apache Software License",
    py_modules=['pyplete'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development",
    ],
)



setup(

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="kate,pate,plugins,kate plugins,pate plugins,python,autocomplete,autocomplete python,django,jquery,js,checker,pep8,pyflakes,jslint",
    include_package_data=True,
    zip_safe=False,
)