# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import View

from .forms import UserLoginForm


class HomePageView(TemplateView):

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']
        return render(request, 'index.html')


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'login/login.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('base:index')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                login(request, user)
                return redirect('base:index')

        return render(request, self.template_name, {'form': form})
