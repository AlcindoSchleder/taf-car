# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control line-input', 'placeholder': 'Nome de usuário'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control line-input', 'placeholder': 'Senha'}),
        }
        labels = {
            'username': 'person',
            'password': 'lock',
        }

    # Validar/autenticar campos de login
    def clean(self):
        username = self.cleaned_data.get('username')
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
