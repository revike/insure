from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from auth_app.models import CompanyUserProfile
from cabinet_app.forms import CompanyProfileCreateForm
from main_app.models import ProductCategory


class CabinetIndexView(CreateView):
    """Контроллер главной страница личного кабинета"""
    template_name = 'cabinet_app/profile.html'
    form_class = CompanyProfileCreateForm

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        company_id = self.request.user.id
        company = CompanyUserProfile.objects
        context['title'] = 'личный кабинет'
        context['categories'] = ProductCategory.get_categories()
        context['company'] = company.filter(
            company__id=company_id, is_active=True,
            company__is_active=True).first()
        context['company_not_active'] = company.filter(
            company__id=company_id, is_active=False, company__is_active=True)
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
