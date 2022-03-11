from django.contrib import auth
from django.contrib.auth import logout, login
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from auth_app.forms import CompanyUserRegisterForm, CompanyUserLoginForm
from auth_app.models import CompanyUser
from auth_app.tasks import send_verify_email
from main_app.models import ProductCategory


class RegisterView(CreateView):
    """Контроллер регистрации"""
    template_name = 'auth_app/register.html'
    form_class = CompanyUserRegisterForm
    success_url = reverse_lazy('main_app:products')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'регистрация'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('cab_app:profile'))
        return super().get(self.request, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            send_verify_email.delay(email=user.email,
                                    activation_key=user.activation_key,
                                    username=user.username)
            self.request.session['register'] = True
            return HttpResponseRedirect(reverse('auth_app:register_valid'))


class RegisterValidView(TemplateView):
    """Контроллер удачной регистрации"""
    template_name = 'auth_app/register_valid.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'регистрация'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get(self, request, *args, **kwargs):
        try:
            if self.request.session['register']:
                self.request.session['register'] = False
                return super().get(self.request, **kwargs)
        except KeyError:
            return HttpResponseRedirect(reverse('main_app:index'))


class VerifyView(TemplateView):
    """Контроллер Верификации"""
    template_name = 'auth_app/verification.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'верификация'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get(self, request, *args, **kwargs):
        user = CompanyUser.objects.filter(email=self.kwargs['email']).first()
        try:
            if user.activation_key == self.kwargs['activation_key']:
                if not user.is_activation_key_expired():
                    user.activation_key = ''
                    user.is_active = True
                    user.save()
                    auth.login(request, user)
                    return super().get(self.request)
                else:
                    user.delete()
        except AttributeError:
            ...
        return HttpResponseRedirect(reverse('main_app:index'))


class LoginUserView(LoginView):
    """Login CompanyUser"""
    template_name = 'auth_app/login.html'
    form_class = CompanyUserLoginForm
    success_url = reverse_lazy('main_app:index')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        next_url = self.request.META.get('HTTP_REFERER')
        self.request.session['next_url'] = next_url
        context = super().get_context_data(**kwargs)
        context['title'] = 'авторизация'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('cab_app:profile'))
        return super().get(self.request, **kwargs)

    def form_valid(self, form):
        next_url = self.request.session['next_url']
        login(self.request, form.get_user())
        if next_url:
            return HttpResponseRedirect(self.request.session['next_url'])
        return HttpResponseRedirect(reverse('cab_app:profile'))


class LogoutUserView(LogoutView):
    """Logout CompanyUser"""

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('auth_app:login'))
