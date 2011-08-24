# -*- coding: utf-8 -
#
# This file is part of fserve released under the MIT license. 
# See the NOTICE for more information.

import os
try:
    import argparse
except ImportError:
    raise ImportError("""\
            argparse module is missing. Try one of this command to
            install it:

            easy_install argparse

            pip install argparse""")


from pistil.tcp.arbiter import TcpArbiter
from pistil.util import parse_address

from fserve import util
from fserve.serve import HttpWorker

def run_server():
    parser = argparse.ArgumentParser(
            description='serve a static file folder')

    parser.add_argument('path', type=str, help='Folder to serve',
            default=".", nargs='?')

    parser.add_argument(
        '--bind', 
        type=str, 
        default="127.0.0.1:5000",
        help="""\
            The socket to bind.
            
            A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'. An IP is a valid
            HOST.
            """)

    parser.add_argument(
            '--workers', 
            type=int, 
            default=1,
            help='Number of workers')

    parser.add_argument(
            '--debug', 
            action='store_true', 
            default=False,
            help='Debug mode')
    
    args = parser.parse_args()

    
    path = args.path
    if path == ".":
        path = os.getcwd()

    address  = parse_address(util.to_bytestring(args.bind))
    conf = {"address": address, "debug": args.debug,
            "num_workers": args.workers}

    spec = (HttpWorker, 30, "send_file", {"path": path}, "worker",)
    
    arbiter = TcpArbiter(conf, spec)
    arbiter.run()


