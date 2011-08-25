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

BLKSIZE = 0x3FFFFFFF

try:
    # Python 3.3 has os.sendfile().
    from os import sendfile
except ImportError:
    try:
        from _sendfile import sendfile
    except ImportError:
        sendfile = None


def sendfile_all(fileno, sockno, offset, nbytes):
    sent = 0
    sent += sendfile(sockno, fileno, offset+sent, nbytes-sent)
    while sent < nbytes:
        sent += sendfile(sockno, fileno, offset+sent, nbytes-sent)

class HttpWorker(TcpGeventWorker):

    def handle(self, sock, addr):
        sock.setblocking(1)
        try:
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
                fno = None
                try:
                    fno = os.open(real_path,
                            os.O_RDONLY|os.O_NONBLOCK)
                    clen = int(os.fstat(fno)[6])
                    
                    # send headers
                    sock.send("".join(["HTTP/1.1 200 OK\r\n", 
                                "Content-Type: " + ctype + "\r\n",
                                "Content-Length:" + str(clen) + "\r\n",
                                 "Connection: close\r\n\r\n"]))

                    if not sendfile:
                        while True:
                            data = os.read(fno, 4096)
                            if not data:
                                break
                            sock.send(data)
                    else:
                        offset = 0
                        nbytes = clen

                        if nbytes > BLKSIZE:
                            # Send file in at most 1GB blocks as some operating
                            # systems can have problems with sending files in blocks
                            # over 2GB.
                            for m in range(0, nbytes, BLKSIZE):
                                sendfile_all(fno, sock.fileno(), offset, 
                                        min(nbytes, BLKSIZE))
                                offset += BLKSIZE
                                nbytes -= BLKSIZE
                        else:
                            sendfile_all(fno, sock.fileno(), offset,
                                    nbytes)
                finally:
                    if fno is not None:
                        os.close(fno)
        finally:
            # make sure we close the socket
            try:
                sock.close()
            except:
                pass
