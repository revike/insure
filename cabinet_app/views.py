from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main_app.models import ProductCategory


class CabinetIndexView(TemplateView):
    """Контроллер главной страница личного кабинета"""
    template_name = 'cabinet_app/index.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'личный кабинет'
        context['categories'] = ProductCategory.get_categories()
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
