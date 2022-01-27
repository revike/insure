import random
from django.views.generic import TemplateView, DetailView, ListView
from main_app.models import ProductCategory, ProductOption


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная'
        context['categories'] = ProductCategory.get_categories()
        return context


class ProductForCategoryDetailView(DetailView):
    """Контроллер списка продуктов для категории"""
    model = ProductCategory
    template_name = 'main_app/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['categories'] = self.model.get_categories()
        context['products'] = ProductOption.get_product_for_category(
            category=self.object)
        return context


class ProductListView(ListView):
    """Контроллер списка продуктов"""
    template_name = 'main_app/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_queryset(self):
        queryset = ProductOption.objects.all()
        return random.sample(list(queryset), queryset.count())
