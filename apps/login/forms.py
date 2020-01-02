# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UsersOperation

# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UsersOperation


class UserLoginForm(forms.ModelForm):

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
        username = self.cleaned_data.get('password')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Usuário ou senha inválidos.")
        return self.cleaned_data

    def authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Usuário ou senha inválidos.")
        return user


class CollectorRegisterForm(forms.ModelForm):
    flag_tuser = forms.HiddenInput()
    user_integration = forms.IntegerField(label='Código no E.R.P.', help_text='Código no E.R.P.')
    first_name = forms.CharField(max_length=100, label='Primeiro Nome', help_text='Primeiro Nome')
    last_name = forms.CharField(max_length=100, label='Sobrenome', help_text='Sobrenome')
    email = forms.EmailField(max_length=150, label='e-Mail', help_text='e-Mail')

    class Meta:
        model = UsersOperation
        fields = ('user_integration', 'first_name', 'last_name', 'email', )
