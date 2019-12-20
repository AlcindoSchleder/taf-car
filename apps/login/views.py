from django.contrib.auth import login
from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import UserLoginForm


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'login/login.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('home:index')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['password']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user:
                login(request, user)
                return redirect('carriers:index')

        return render(request, self.template_name, {'form': form})
