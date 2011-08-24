# -*- coding: utf-8 -
#
# This file is part of fserve released under the MIT license. 
# See the NOTICE for more information.




# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license. 
# See the NOTICE for more information.

import mimetypes
import os


from gevent import monkey
monkey.noisy = False
monkey.patch_all()


from http_parser.http import HttpStream
from http_parser.reader import SocketReader

from pistil import util
from pistil.tcp.gevent_worker import TcpGeventWorker

CURDIR = os.path.dirname(__file__)

try:
    # Python 3.3 has os.sendfile().
    from os import sendfile
except ImportError:
    try:
        from _sendfile import sendfile
    except ImportError:
        sendfile = None


class HttpWorker(TcpGeventWorker):

    def handle(self, sock, addr):
        p = HttpStream(SocketReader(sock))

        path = p.path()

        if not path or path == "/":
            path = "index.html"
        
        if path.startswith("/"):
            path = path[1:]
        
        real_path = os.path.join(self.conf['path'], path)

        if os.path.isdir(real_path):
            lines = ["<ul>"]
            for d in os.listdir(real_path):
                fpath = os.path.join(real_path, d)
                lines.append("<li><a href=" + d + ">" + d + "</a>")

            data = "".join(lines)
            resp = "".join(["HTTP/1.1 200 OK\r\n", 
                            "Content-Type: text/html\r\n",
                            "Content-Length:" + str(len(data)) + "\r\n",
                            "Connection: close\r\n\r\n",
                            data])
            sock.sendall(resp)

        elif not os.path.exists(real_path):
            util.write_error(sock, 404, "Not found", real_path + " not found")
        else:
            ctype = mimetypes.guess_type(real_path)[0]
            if ctype.startswith('text') or 'html' in ctype:

                try:
                    f = open(real_path, 'rb')
                    data = f.read()
                    resp = "".join(["HTTP/1.1 200 OK\r\n", 
                                "Content-Type: " + ctype + "\r\n",
                                "Content-Length:" + str(len(data)) + "\r\n",
                                "Connection: close\r\n\r\n",
                                data])
                    sock.sendall(resp)
                finally:
                    f.close()
            else:

                try:
                    f = open(real_path, 'r')
                    clen = int(os.fstat(f.fileno())[6])
                    
                    # send headers
                    sock.send("".join(["HTTP/1.1 200 OK\r\n", 
                                "Content-Type: " + ctype + "\r\n",
                                "Content-Length:" + str(clen) + "\r\n",
                                 "Connection: close\r\n\r\n"]))

                    if not sendfile:
                        while True:
                            data = f.read(4096)
                            if not data:
                                break
                            sock.send(data)
                    else:
                        fileno = f.fileno()
                        sockno = sock.fileno()
                        sent = 0
                        offset = 0
                        nbytes = clen
                        sent += sendfile(sockno, fileno, offset+sent, nbytes-sent)
                        while sent != nbytes:
                            sent += sendfile(sock.fileno(), fileno, offset+sent, nbytes-sent)


                finally:
                    f.close()
