from dataclasses import asdict
import os

from setuptools import setup
from setuptools import find_packages

here = os.path.join(os.path.dirname(__file__))


__version__ = None
with open(os.path.join(here, 'valorant', 'version.py')) as _file:
    exec(_file.read())

with open(os.path.join(here, 'requirements', 'core.txt')) as _file:
    REQUIREMENTS = _file.read().splitlines()

with open(os.path.join(here, 'requirements', 'test.txt')) as _file:
    TEST_REQUIREMENTS = _file.read().splitlines()
    TEST_REQUIREMENTS = list(set(REQUIREMENTS + TEST_REQUIREMENTS))

with open(os.path.join(here, 'README.md')) as _file:
    README = _file.read()

with open(os.path.join(here, 'CHANGELOG.md')) as _file:
    CHANGELOG = _file.read()

about_text = (
    'Coming soon.',
    'I promise.'
)

print('FIND_ME: ' + ','.join(REQUIREMENTS))

setup(
    name='unofficial-valorant-api-py',
    version=__version__,
    description='Python SDK for Henrik Dev Unofficial Valorant API (https://docs.henrikdev.xyz/valorant.html)',
    long_description=about_text + README + CHANGELOG,
    long_description_type='text/markdown',
    author='brendanorourke',
    url='https://github.com/brendanorourke/unofficial-valorant-api-py',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    extras_require={'test': TEST_REQUIREMENTS},
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='tests'
)