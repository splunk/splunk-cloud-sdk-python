# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

from setuptools import setup, find_packages
from splunk_sdk import __version__

install_requires = ['requests=2.20.1',
                    'urllib3=1.24.1', ]

setup(
    name='splunk-cloud-sdk-python',
    version=__version__,
    description='SDK for the Splunk Developer Cloud platform',
    long_description='A .',
    author='Splunk',
    author_email='dev@splunk.com',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha', ],
    keywords='',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={
        'dev': ['pep8>=1.7.1',
                'pylint>=1.6.4',
                ],
        'test': ['coverage>=4.2', ],
    },
)
