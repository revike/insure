from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from auth_app.forms import CompanyUserRegisterForm
from auth_app.models import CompanyUser
from auth_app.service import send_verify_email
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

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('main_app:products'))


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
        user = CompanyUser.objects.get(email=self.kwargs['email'])
        if user.activation_key == self.kwargs['activation_key'] \
                and not user.is_activation_key_expired():
            user.activation_key = ''
            user.is_active = True
            user.save()
            auth.login(request, user)
        return super().get(self.request)


class LoginUserView(LoginView):
    """Login CompanyUser"""
    template_name = 'auth_app/login.html'
    form_class = ...
    success_url = ...

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'авторизация'
        context['categories'] = ProductCategory.get_categories()
        return context


class LogoutUserView(LogoutView):
    """Logout CompanyUser"""

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('auth_app:login'))
