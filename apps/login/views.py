import apps
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
            apps.CAR_LOADED = False
            return redirect('carriers:carriers', carid=apps.CAR_ID, loaded=apps.CAR_LOADED)
        return render(request, self.template_name, {'form': form, 'cardid': apps.CAR_ID})

    def post(self, request):
        message = '';
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['password']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            try:
                if user is not None:
                    login(request, user)
                    return redirect('carriers:carriers')
                elif form.flag_ins:
                    return redirect('login:signup')
                else:
                    message = 'Error: Usuário não encontrado ou não possui atividades até agora!'
            except Exception as e:
                code = form.result['status']['sttCode']
                message = f'Error: Login user exception: ({code}) - {e}'

        return render(request, self.template_name, {'form': form, 'cardid': apps.CAR_ID, 'message': message})


class CollectorRegisterView(View):
    form_class = CollectorRegisterForm
    template_name = 'login/signup.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('carriers:carriers')
        return render(request, self.template_name, {'form': form, 'carid': apps.CAR_ID})

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
                operator = UsersOperators()
                operator.fk_cars.pk = apps.CAR_ID
                operator.
                operator.flag_tuser = 4
                user.save()
                # operator.user_integration = form.cleaned_data.get('username')
                # operator.save()
                # TODO: 1) get user permissions and save it.
                #       2) Verify if user has activities and hour initial / hour end
                #       3) Yes: redirect to carriers
                #       4) No: render a message that user not has a activity to do
        else:
            form = self.form_class()
        return render(request, 'signup.html', {'form': form})
