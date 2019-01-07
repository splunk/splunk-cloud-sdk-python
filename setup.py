from setuptools import setup, find_packages
from splunk_sdk import __version__

install_requires = ['requests>=2.20.0',
                    'urllib3>=1.24', ]

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
