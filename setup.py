#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt', 'r') as fd:
    requirements = list(filter(lambda r: not r.strip().startswith('#'), fd.readlines()))

test_requirements = requirements


setup(
    name='vulyk_ner',
    version='0.1.0',
    description="Vulyk NER tagging plugin. Based on works of Brat Rapid Annotation Tool ((c) 2010-2012 The brat contributors)",
    long_description=readme + '\n\n' + history,
    author="Dmitry Chaplinsky",
    author_email='chaplinsky.dmitry@gmail.com',
    url='https://github.com/hotsyk/vulyk-tagging',
    packages=[
        'vulyk_ner',
        'vulyk_ner.models',
        'vulyk_ner.static',
    ],
    package_dir={'vulyk_ner':
                 'vulyk_ner'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='vulyk_ner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    scripts=[],
)
