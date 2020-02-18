# -*- coding: utf-8 -*-
import socket
import time


class CheckHost:
    _HOSTS = {}

    _PORT = 5180
    _TIMEOUT = 1.5

    _client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, hosts: dict):
        self._HOSTS = hosts if len(hosts) > 0 else {}
        self._client.settimeout(self._TIMEOUT)

    def _try_hosts(self):
        for host in self._HOSTS:
            try:
                self._client.connect((self._HOSTS[host], int(self._PORT)))
                self._client.shutdown(socket.SHUT_RDWR)
                return self._HOSTS[host]
            except Exception as e:
                time.sleep(1)
            finally:
                self._client.shutdown(socket.SHUT_RDWR)
        return None

    def check_hosts(self):
        return self._try_hosts()
