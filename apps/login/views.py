import apps
from django.contrib.auth import login
from django.views.generic import View
from django.shortcuts import render, redirect
from datetime import datetime, time
from .forms import User, UserLoginForm, CollectorRegisterForm
from .models import UsersOperators, UsersOperatorsPermissions
from apps.carriers.models import Cars


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
        message = ''
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
                    apps.USER_NAME = username
                    apps.USER_DATA = form.result
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
    user_data = None

    def get(self, request):
        form = self.form_class(None)
        self.user_data = apps.USER_DATA

        if request.user.is_authenticated:
            return redirect('carriers:carriers')
        return render(request, self.template_name, {'form': form, 'carid': apps.CAR_ID})

    def post(self, request):
        self.user_data = apps.USER_DATA
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                operator = form.save(commit=False)
                cars = Cars.objects.get(pk=apps.CAR_ID)
                # operator = UsersOperators()
                operator.first_name = form.cleaned_data.get('first_name')
                operator.last_name = form.cleaned_data.get('last_name')
                operator.email = form.cleaned_data.get('email')
                operator.flag_tuser = 4
                operator.user_integration = form.cleaned_data.get('username')
                # Fields get from external API
                operator.fk_cars = cars
                operator.nroempresa = self.user_data['records'][0]['nroempresa']
                operator.tipprodutivo = self.user_data['records'][0]['tipprodutivo']
                operator.statusprodutivo = self.user_data['records'][0]['statusprodutivo']
                operator.inddisponibilidade = self.user_data['records'][0]['inddisponibilidade']
                clock = datetime.time(datetime.strptime(
                    self.user_data['records'][0]['horinijornada'], '%H%M'
                ))
                operator.horinijornada = clock
                clock = datetime.time(datetime.strptime(
                    self.user_data['records'][0]['horfimjornada'], '%H%M'
                ))
                operator.horfimjornada = clock

                user = User()
                user.username = apps.USER_NAME
                user.password = apps.USER_NAME
                # user.profile.first_name = form.cleaned_data.get('first_name')
                # user.profile.last_name = form.cleaned_data.get('last_name')
                # user.profile.email = form.cleaned_data.get('email')
                # user can't login until get a new Activity
                user.is_active = True
                user.save()
                user.refresh_from_db()
                operator.save()
                # Validade user data
                time = datetime.now().time()
                # TODO: Retirar até 2a. ordem
                # if operator.horinijornada < time or operator.horfimjornada > time:
                #     message = 'Usuário não está no horário de serviço!'
                #     message += f'(início: {operator.horinijornada} - fim: {operator.horfimjornada})'
                #     return redirect('login:login', message=message)
                if operator.inddisponibilidade == 'N':
                    message = 'Usuário não está disponível no momentp!'
                    message += f'(flag disponivel: {operator.inddisponibilidade})'
                    return redirect('login:login', message=message)

                # Save user permissions
                for data in self.user_data:
                    perms = UsersOperatorsPermissions()
                    perms.pk_user_permissions = f'{operator.user_integration}-{self.user_data[data]["codlinhasepar"]}'
                    perms.codlinhasepar = self.user_data[data]['codlinhasepar']
                    perms.desclinhasepar = self.user_data[data]['desclinhasepar']
                    perms.indseparacao = self.user_data[data]['indseparacao']
                    perms.ls_status = self.user_data[data]['ls_status']
                    perms.save()
                    apps.USER_PERMISSIONS.append(perms.codlinhasepar)

                return redirect('carriers:carriers')
        else:
            form = self.form_class()
        return render(request, 'signup.html', {'form': form})
