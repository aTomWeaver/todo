#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='td',
      version='1.0',
      description='A simple CLI todo app',
      author='tom weaver',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'td = todo.td:main'
        ]
      }
      )
