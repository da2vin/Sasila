#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='sasila',
        version='0.0.3',
        description=(
            'a simple spider system'
        ),
        long_description=open('README-SETUP.rst').read(),
        author='DaVinciDW',
        author_email='darkwings_love@163.com',
        maintainer='DaVinciDW',
        maintainer_email='darkwings_love@163.com',
        license='MIT License',
        packages=find_packages(),
        platforms=["all"],
        url='https://github.com/DarkSand/Sasila',
        install_requires=[
            'Flask>=0.11.1',
            'redis>=2.10.5',
            'requests>=2.13.0',
            'six>=1.10.0',
            'SQLAlchemy>=1.1.4',
            'grequests>=0.3.0',
            'selenium>=2.53.6',
            'lxml>=3.7.2',
            'beautifulsoup4>=4.6.0',
        ],
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Text Processing :: Indexing",
            "Topic :: Utilities",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
        ],
)
