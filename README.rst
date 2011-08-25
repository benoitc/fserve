fserve
------

Simple and efficient way to serve static file. used as a pistil
demonstration. Handle sendifle api is available on your system.

Requirements
++++++++++++

- Python 2.5 or sup.
- Gevent > 0.13
- Pistil >= 0.1.0
- http-parser >= 0.6.3

Note: To set the process name, install the library setproctitle:

::

    $ ps ax|grep test_cors
    78064 s002  S+     0:00.35 arbiter [test_cors running 3 workers]     
    78065 s002  S+     0:00.10 worker test_cors [78065]     
    78066 s002  S+     0:00.11 worker test_cors [78066]     
    78067 s002  S+     0:00.09 worker test_cors [78067] 

Installation
++++++++++++

Do one of this command to install it from pypi

::

    pip install fserve

or::

    easy_install fserve

From source do::

    $ git clone git://github.com/benoitc/fserve.git
    $ cd fserve && python setup.py install


Usage
+++++

::

    $ fserve [-h] [--bind BIND] [--workers WORKERS] [--debug] [path]

    serve a static file folder

    positional arguments:
      path               Folder to serve

    optional arguments:
      -h, --help         show this help message and exit
      --bind BIND        The socket to bind. A string of the form: 'HOST',
                         'HOST:PORT', 'unix:PATH'. An IP is a valid HOST.
      --name NAME        name of the server
      --workers WORKERS  Number of workers
    --debug            Debug mode

Example:

In your source folder::

    $ cd examples/static
    $ fserve --workers 3

And go on http://127.0.0.1:5000 url .
