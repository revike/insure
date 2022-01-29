from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from main_app.models import ProductCategory, ProductOption


class IndexView(TemplateView):
    """Контроллер главной страницы"""
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        """Получить контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная'
        context['categories'] = ProductCategory.get_categories()
        return context


class ProductForCategoryDetailView(ListView):
    """Контроллер списка продуктов для категории"""
    model = ProductCategory
    template_name = 'main_app/category.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получить контекст для этого представления"""
        queryset = ProductOption.get_product_for_category(
            category=self.kwargs['pk']).select_related()
        context = super().get_context_data(**kwargs, object_list=queryset)
        categories = ProductCategory.get_categories()
        context['title'] = categories.filter(id=self.kwargs['pk']).first()
        context['categories'] = categories
        return context

    def get_queryset(self):
        """Возвращает список элементов для этого представления"""
        return get_object_or_404(self.model, pk=self.kwargs['pk'],
                                 is_active=True)


class ProductListView(ListView):
    """Контроллер списка продуктов"""
    template_name = 'main_app/products.html'
    model = ProductOption
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получить контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_queryset(self):
        """Возвращает список элементов для этого представления"""
        return ProductOption.objects.filter(
            is_active=True,
            product__is_active=True,
            product__category__is_active=True).select_related()

    def get(self, request, *args, **kwargs):
        category_filter = []
        request_get = self.request.GET

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        categories = context['categories']

        for category in categories:
            if request_get.get(category.name) is not None:
                category_filter.append(category)

        min_price = request_get.get('min_price')
        max_price = request_get.get('max_price')
        min_term = request_get.get('min_term')
        max_term = request_get.get('max_term')
        min_rate = request_get.get('min_rate')
        max_rate = request_get.get('max_rate')

        if category_filter:
            self.object_list = self.object_list.filter(
                product__category__in=category_filter)
        if min_price:
            self.object_list = self.object_list.filter(price__gte=min_price)
        if max_price:
            self.object_list = self.object_list.filter(price__lte=max_price)
        if min_term:
            self.object_list = self.object_list.filter(term__gte=min_term)
        if max_term:
            self.object_list = self.object_list.filter(term__lte=max_term)
        if min_rate:
            self.object_list = self.object_list.filter(rate__gte=min_rate)
        if max_rate:
            self.object_list = self.object_list.filter(rate__lte=max_rate)

        context = self.get_context_data()
        return self.render_to_response(context)
