from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from main_app.models import ProductCategory, ProductOption


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная'
        context['categories'] = ProductCategory.get_categories()
        return context


class ProductForCategoryDetailView(ListView):
    """Контроллер списка продуктов для категории"""
    model = ProductCategory
    template_name = 'main_app/category.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        queryset = ProductOption.get_product_for_category(
            category=self.kwargs['pk'])
        context = super().get_context_data(**kwargs, object_list=queryset)
        categories = ProductCategory.get_categories()
        context['title'] = categories.filter(id=self.kwargs['pk']).first()
        context['categories'] = categories
        return context

    def get_queryset(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'],
                                 is_active=True)


class ProductListView(ListView):
    """Контроллер списка продуктов"""
    template_name = 'main_app/products.html'
    model = ProductOption
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты'
        context['categories'] = ProductCategory.get_categories()
        return context
