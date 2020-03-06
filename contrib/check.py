# -*- coding: utf-8 -*-
import socket
from apps.home.models import ApiHosts


class CheckHost:
    _PORT = 5180
    _TIMEOUT = 1.5
    _client = None

    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.settimeout(self._TIMEOUT)

    def _try_hosts(self, host: str):
        try:
            self._client.connect((self._HOSTS[host], int(self._PORT)))
            self._client.shutdown(socket.SHUT_RDWR)
            self._client.close()
            return self._HOSTS[host]
        except socket.error:
            self._client.shutdown(socket.SHUT_RDWR)
            self._client.close()
            return None
        finally:
            self._client.shutdown(socket.SHUT_RDWR)
            self._client.close()

    def check_hosts(self):
        server = None
        host = ApiHosts.objects.get(flag_active=1)
        server = self._try_hosts(host)
        return server
