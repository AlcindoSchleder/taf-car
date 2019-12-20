# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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
