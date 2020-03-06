import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.views.generic import View
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import User, UserLoginForm, CollectorRegisterForm
from .models import UsersOperators, UsersOperatorsPermissions
from apps.carriers.models import Cars


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'login/login.html'
    message = None

    def get(self, request):
        apps.CAR_ID = request.session.get('car_id')
        form = self.form_class(None)

        if request.user.is_authenticated:
            apps.CAR_COLLECT_PRODUCTS = True
            params = {
                'car_id': 1,
                'car_prepared': 1,
                'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
                'user': request.user.username,
                'message': ''
            }
            return redirect(apps.get_redirect_url('carriers:carriers', params=params))

        return render(request, self.template_name, {'form': form, 'car_id': apps.CAR_ID})

    def post(self, request):
        apps.CAR_ID = request.session.get('car_id')
        if self.message:
            message = self.message
        else:
            message = ''
        self.message = ''
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['password']
            password = form.cleaned_data['password']
            res = form.authenticate_user(username=username, password=password)
            try:
                user = res['user']
                apps.USER_NAME = username
                apps.USER_DATA = res['records'] if 'records' in res.keys() else None
                if user is not None:
                    login(request, user)
                    apps.CAR_COLLECT_PRODUCTS = True
                    params = {
                        'car_id': apps.CAR_ID,
                        'car_prepared': 1,
                        'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
                        'user': request.user.username,
                        'message': ''
                    }
                    return redirect(apps.get_redirect_url('carriers:carriers', params))
                elif form.flag_ins:
                    params = {
                        'car_id': apps.CAR_ID,
                        'message': '',
                        'user_data': apps.USER_DATA[0]
                    }
                    return redirect(apps.get_redirect_url('login:signup', params))
                else:
                    apps.USER_NAME = None
                    apps.USER_DATA = None
                    message = 'Error: Usuário não encontrado ou não possui atividades até agora!'
            except Exception as e:
                code = res['status']['sttCode']
                message = f'Error: Login user exception: ({code}) - {e}'

        return render(request, self.template_name, {'form': form, 'car_id': apps.CAR_ID, 'message': message})


class CollectorRegisterView(View):
    form_class = CollectorRegisterForm
    template_name = 'login/signup.html'
    user_data = None

    def _get_initial(self):
        if self.user_data is not None:
            data = self.user_data[0]
            mail_name = str(data['produtivo']).split(' ')[0].lower()
            return {
                'user_integration': data['codprodutivo'],
                'first_name': str(data['produtivo']).split(' ')[0],
                'last_name': ' '.join(data['produtivo'].split(' ')[1:]),
                'email': f'{mail_name}.operador@tafdistribuidora.com.br'
            }
        return None

    def get(self, request):
        self.user_data = apps.USER_DATA
        initial_data = self._get_initial()
        apps.CAR_ID = request.session.get('car_id')

        form = self.form_class(initial_data)

        if request.user.is_authenticated:
            params = {
                'car_id': apps.CAR_ID,
                'car_prepared': 1,
                'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
                'user': request.user.username,
                'message': ''
            }
            return redirect(apps.get_redirect_url('carriers:carriers', params))
        return render(request, self.template_name, {'form': form, 'car_id': apps.CAR_ID})

    def save_user_operators(self, form):
        operator = form.save(commit=False)
        cars = Cars.objects.get(pk=apps.CAR_ID)
        # operator = UsersOperators()
        operator.first_name = form.cleaned_data.get('first_name')
        operator.last_name = form.cleaned_data.get('last_name')
        operator.email = form.cleaned_data.get('email')
        operator.flag_tuser = 4
        operator.user_integration = form.cleaned_data.get('user_integration')
        # Fields get from external API
        operator.fk_cars = cars
        operator.nroempresa = self.user_data[0]['nroempresa']
        operator.tipprodutivo = self.user_data[0]['tipprodutivo']
        operator.statusprodutivo = self.user_data[0]['statusprodutivo']
        operator.inddisponibilidade = self.user_data[0]['inddisponibilidade']
        operator.user_integration = apps.USER_NAME
        clock = datetime.time(datetime.strptime(
            self.user_data[0]['horinijornada'], '%H%M'
        ))
        operator.horinijornada = clock
        clock = datetime.time(datetime.strptime(
            self.user_data[0]['horfimjornada'], '%H%M'
        ))
        operator.horfimjornada = clock
        # Save User into django auth
        user = User()
        user.username = apps.USER_NAME
        user.password = make_password(apps.USER_NAME)
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        # user can't login until get a new Activity
        user.is_active = True
        user.save()
        user.refresh_from_db()
        # Save operator Data
        operator.save()
        return operator

    def check_operator_rules(self, operator) -> str:
        # Check operator
        self.message = ''
        if operator.horinijornada < datetime.now().time() or operator.horfimjornada > datetime.now().time():
            self.message = 'Usuário não está no horário de serviço!<br />'
            self.message += f'(início: {operator.horinijornada} - fim: {operator.horfimjornada})'
        if operator.inddisponibilidade == 'N':
            self.message = 'Usuário não está disponível no momentp!<br />'
            self.message += f'(flag disponivel: {operator.inddisponibilidade})'
        return self.message

    def post(self, request):
        self.user_data = apps.USER_DATA
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                operator = self.save_user_operators(form)
                message = self.check_operator_rules(operator)
                if message:
                    params = {
                        'car_id': apps.CAR_ID,
                        'car_prepared': 1,
                        'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
                        'message': ''
                    }
                    return redirect(apps.get_redirect_url('login:login', params))
                # Save user permissions
                for data in self.user_data:
                    user = User.objects.get(pk=operator.user_integration)
                    perms = UsersOperatorsPermissions()
                    perms.pk_user_permissions = f'{operator.user_integration}-{data["codlinhasepar"]}'
                    perms.fk_users = user
                    perms.type_line = data['codlinhasepar']
                    perms.dsc_line = data['desclinhasepar']
                    perms.flag_separation = data['indseparacao']
                    perms.flag_status = data['ls_status']
                    perms.save()
                    apps.USER_PERMISSIONS.append(perms.type_line)

                params = {
                    'car_id': apps.CAR_ID,
                    'car_prepared': 1,
                    'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
                    'user': operator.user_integration,
                    'message': '',
                }
                return redirect(apps.get_redirect_url('carriers:carriers', params))
        else:
            initial_data = self._get_initial()
            form = self.form_class(initial_data)
        params = {
            'form': form,
            'car_id': apps.CAR_ID,
            'message': ''
        }
        return render(request, 'signup.html', params)
