
from setuptools import setup, find_packages
from bubka import __version__

setup(
    name='bubka',
    keywords='rest api python client',
    description='Command line client for REST APIs',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://github.com/hile/bubka/',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bubka=bubka.bin.bubka:main',
        ],
    },
    install_requires=(
        'systematic>=4.8.4',
    ),
    tests_require=(
        'pytest',
        'pytest-runner',
        'pytest-datafiles',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
