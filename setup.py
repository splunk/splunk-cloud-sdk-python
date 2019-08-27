# coding: utf-8

# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages
from splunk_sdk import __version__

install_requires = ['requests>=2.22.0,<2.23',
                    'urllib3>=1.25.2,<1.26', ]

setup(
    name='splunk-cloud-sdk',
    version=__version__,
    description='SDK for the Splunk Developer Cloud platform',
    author='Splunk',
    author_email='dev@splunk.com',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha', ],
    keywords='',
    packages=find_packages(exclude=['test']),
    install_requires=install_requires,
    setup_requires=[
        'setuptools',
        'setuptools-git',
        'wheel'
    ],
    extras_require={
        'dev': ['pep8>=1.7.1,<2',
                'sphinx >= 2.0.1,<3',
                'sphinxcontrib-apidoc>=0.3.0',
                'cryptography>=2.6.1,<2.7',
                ],
        'test': ['coverage>=4.5.3,<5',
                 'flake8>=3.7.7,<4',
                 'pytest>=4.4.0,<5',
                 ],
    },
)
