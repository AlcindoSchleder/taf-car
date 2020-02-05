from django.contrib.auth import login
from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import UserLoginForm, CollectorRegisterForm
from .models import UsersOperators


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'login/login.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('carriers:carriers')
        return render(request, self.template_name, {'form': form, 'data': data})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['password']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('carriers:carriers')
            elif form.flag_ins:
                return redirect('login:signup')

        return render(request, self.template_name, {'form': form})


class CollectorRegisterView(View):
    form_class = CollectorRegisterForm
    template_name = 'login/signup.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('carriers:carriers')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')
                # user can't login until get a new Activity
                user.is_active = False
                user.save()
                UsersOperators.flag_tuser = 4
                UsersOperators.user_integration = form.cleaned_data.get('username')
                UsersOperators.save()
                # TODO: 1) get user permissions and save it.
                #       2) Verify if user has activities and hour initial / hour end
                #       3) Yes: redirect to carriers
                #       4) No: render a message that user not has a activity to do
        else:
            form = self.form_class()
        return render(request, 'signup.html', {'form': form})
