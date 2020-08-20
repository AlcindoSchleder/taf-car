# -*- coding: utf-8 -*-
"""
    taf_car User authentication baackend
"""
import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class SettingsBackend(BaseBackend):
    """
    Authenticate user with call a request on api that return if user exists
    """
    def call_api(self, request, *args, **kwargs):
        # headers = {
        #     'token': 'get token',
        # }
        url = 'http://192.168.0.203/operators/' + args[0]
        response = requests.get(url)
        res = response.json()
        return res['username']

    def authenticate(self, request, username=None, password=None):
        login_valid = self.call_api([username]) and check_password(password)
        if login_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise Exception('Operador não encontrado!')
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
