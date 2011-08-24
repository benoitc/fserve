# -*- coding: utf-8 -
#
# This file is part of fserve released under the MIT license. 
# See the NOTICE for more information.

import os

from setuptools import setup

from fserve import __version__

setup(name='fserve',
    version= __version__,
    description = 'serve static file.',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
            )
        ).read(),
    author = 'Benoit Chesneau',
    author_email = 'benoitc@e-engura.com',
    license = 'MIT',
    url = 'http://gunicorn.org',
    packages=['fserve'],
    install_requires=['gevent', 'pistil', 'http-parser'],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Environment :: Other Environment',        
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        ],
    # XXX use distutils' script
    entry_points="""
    [console_scripts]
    fserve = fserve.console:run_server
    """)
