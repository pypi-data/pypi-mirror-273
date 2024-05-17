import logging

import socket
from threading import RLock

from lxdbapi import errors, versions
import ssl

try:
    import httplib
except ImportError:
    import http.client as httplib

__all__ = ['TcpAvaticaConnection', 'NetAvaticaConnection']

logger = logging.getLogger(__name__)

class NetAvaticaConnection(object):
    def close(self):
        raise NotImplementedError('Extend NetAvaticaConnection')

    def request(self, body=None):
        raise NotImplementedError('Extend NetAvaticaConnection')

    def checkSerialization(self):
        raise NotImplementedError('Extend NetAvaticaConnection')


class TcpAvaticaConnection(NetAvaticaConnection):

    def __init__(self, url, secure, max_retries):
        """Opens a FTP connection to the RPC server."""
        self._close_lock = RLock()
        self.url = url
        self.secure =secure
        self.max_retries = max_retries if max_retries is not None else 3
        self._opened = False
        self._connect()

    def __del__(self):
        self._close()

    def __exit__(self):
        self._close()

    def _connect(self):
        if not self.secure:
            logger.debug("Using TCP")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            self.tcp_socket.connect((self.url.hostname, self.url.port))
            self.tcpConn = self.tcp_socket
            self._opened = True
        else:
            logger.debug("Using TCP with SSL")
            logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            self.tcpConn = ssl.wrap_socket(self.tcp_socket)
            self.tcpConn.connect((self.url.hostname, self.url.port))
            self._opened = True

    def _close(self):
        with self._close_lock:
            if self._opened:
                self._opened = False
                self.tcpConn.close()

    def close(self):
        self._close()

    def request(self, body=None):
        req_sz = len(body)
        # build message Body size, tag(always 0), body
        tag = 0
        msg = bytearray()
        msg.extend(req_sz.to_bytes(4, 'little'))
        msg.extend(tag.to_bytes(4, 'little'))
        msg.extend(body)
        self.tcpConn.sendall(msg)
        hdr = self.tcpConn.recv(8)
        resp_sz = int.from_bytes(hdr[:4], 'little')
        tag = int.from_bytes(hdr[4:], 'little')
        if 0 > resp_sz:
            logger.warning("negative msg size (sz {}) tag:{}".format(resp_sz, tag))
            raise IOError('IO Error on RPC request on {}. Got negative size [{}]'.format(self.url, resp_sz))
        if 0 == resp_sz:
            return None
        response = bytearray()
        pending = resp_sz
        offset = 0
        while pending > 0:
            partial = self.tcpConn.recv(resp_sz)
            if partial is None:
                raise IOError("No data. Connection closed")
            l = len(partial)
            if l <= 0:
                raise IOError("No data. Connection closed")
            offset += l
            pending -= l
            response.extend(partial)
        return response

    def checkSerialization(self):
        raise NotImplementedError('Should use server-info. Cotact support')