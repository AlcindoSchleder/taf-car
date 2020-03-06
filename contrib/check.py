# -*- coding: utf-8 -*-
import socket
from apps.home.models import ApiHosts


class CheckHost:
    _TIMEOUT = 1.5
    _client = None

    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.settimeout(self._TIMEOUT)

    def _try_hosts(self, host: str, port: int):
        try:
            self._client.connect((host, port))
            self.host = host
        except socket.error:
            self.host = None
        finally:
            self._client.shutdown(socket.SHUT_RDWR)
            self._client.close()
        return self.host

    def check_hosts(self):
        server = None
        host = ApiHosts.objects.get(flag_active=1)
        server = self._try_hosts(host.address, host.port)
        return server
