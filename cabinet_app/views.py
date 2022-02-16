from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from auth_app.models import CompanyUserProfile, CompanyUser
from cabinet_app.forms import ProfileCreateForm, ProfileUpdateForm, \
    ProfileUpdateDataForm
from main_app.models import ProductCategory


class CabinetIndexView(CreateView):
    """Контроллер главной страница личного кабинета"""
    template_name = 'cabinet_app/profile.html'
    form_class = ProfileCreateForm

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        company_id = self.request.user.id
        company = CompanyUserProfile.objects.filter(
            company__id=company_id, company__is_active=True)
        context['title'] = 'личный кабинет'
        context['categories'] = ProductCategory.get_categories()
        context['company'] = company.filter(is_active=True).select_related()
        context['company_not_active'] = company.filter(
            is_active=False).select_related()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.company = self.request.user
            form.save()
        return HttpResponseRedirect(reverse('cab_app:profile'))

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProfileUpdateView(UpdateView):
    """Контроллер редактирования профиля компании"""
    success_url = reverse_lazy('cab_app:profile')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование профиля'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_template_names(self):
        if self.request.resolver_match.url_name == 'profile_update':
            template_name = 'cabinet_app/profile_update.html'
        else:
            template_name = 'cabinet_app/profile_update_data.html'
        return template_name

    def get_form_class(self):
        if self.request.resolver_match.url_name == 'profile_update':
            form_class = ProfileUpdateForm
        else:
            form_class = ProfileUpdateDataForm
        return form_class

    def get_queryset(self):
        if self.request.resolver_match.url_name == 'profile_update':
            queryset = CompanyUserProfile.objects.filter(
                is_active=True, company__is_active=True)
        else:
            queryset = CompanyUser.objects.filter(
                is_active=True)
        return queryset

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
