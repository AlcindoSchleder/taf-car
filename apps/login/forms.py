# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UsersOperators
from data_control.api import ApiHostAccess

api = ApiHostAccess({})


class UserLoginForm(forms.ModelForm):
    username = None
    password = None
    flag_ins = False
    result = api.result

    HTTP_API_GET_OPERATOR = 'tafApi/login/1.0'

    class Meta:
        model = User
        fields = ('password', )
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control line-input', 'placeholder': 'Senha'}),
        }
        labels = {
            'password': 'Senha: ',
        }

    # Validar/autenticar campos de login
    def clean(self):
        self.flag_ins = False
        self.username = self.cleaned_data.get('password')
        self.password = self.cleaned_data.get('password')
        user = authenticate(username=self.username, password=self.password)
        if not user or not user.is_active:
            self.flag_ins = True
        return self.cleaned_data

    def is_valid(self):
        self.flag_ins = False
        valid = super(UserLoginForm, self).is_valid()
        if not valid:
            self.flag_ins = True
        return valid

    def authenticate_user(self, username=None, password=None):
        self.flag_ins = False
        username = username if username else self.username
        password = password if password else self.password

        user = authenticate(username=username, password=password)
        if not user:
            try:
                api.set_end_points({'login': f'/{self.HTTP_API_GET_OPERATOR}/{username}'})
                res = api.get_data('login')
                if res['status']['sttCode'] == 200:
                    res = res['data']
                    if len(res['records']) > 0 and str(res['records'][0]['codprodutivo']) == password:
                        self.flag_ins = True
                        self.result['records'] = res['records']
                        self.result['flag_ins'] = self.flag_ins
                else:
                    self.result = res
            except Exception as e:
                raise e
        return user


class CollectorRegisterForm(forms.ModelForm):
    flag_tuser = forms.HiddenInput()
    user_integration = forms.IntegerField(label='Código no E.R.P.', help_text='Código no E.R.P.')
    first_name = forms.CharField(max_length=100, label='Primeiro Nome', help_text='Primeiro Nome')
    last_name = forms.CharField(max_length=100, label='Sobrenome', help_text='Sobrenome')
    email = forms.EmailField(max_length=150, label='e-Mail', help_text='e-Mail')

    class Meta:
        model = UsersOperators
        fields = ('user_integration', 'first_name', 'last_name', 'email', )
