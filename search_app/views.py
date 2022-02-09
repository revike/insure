from django.views.generic import TemplateView
from elasticsearch_dsl import Q

from main_app.models import ProductCategory
from search_app.documents import ProductOptionDocument
from search_app.search import search_obj


class SearchView(TemplateView):
    """Elastic поиск"""
    template_name = 'search_app/search.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск по запросу:'
        context['categories'] = ProductCategory.get_categories()

        query = self.request.GET.get('search')

        q = Q(
            'multi_match',
            query=query,
            fields=[
                'product.name', 'product.category.name',
                'product.company.name', 'product.short_desc',
                'product.description',
            ],
            fuzziness='auto',
        )
        search = search_obj(q)

        if search.count() == 0:
            try:
                query = int(query)
                q = Q(
                    'multi_match',
                    query=query,
                    fields=[
                        'price', 'rate', 'term'
                    ]
                )
                search = search_obj(q)
            except ValueError:
                pass

        context['search'] = search

        return context

    def get(self, request, *args, **kwargs):
        return super().get(self.request, **kwargs)


class FilterView(TemplateView):
    """Elastic filter"""
    template_name = 'search_app/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.get_categories()
        request_get = self.request.GET

        category_filter = []
        for category in categories:
            if request_get.get(category.name):
                category_filter.append(category.name)

        min_price = request_get.get('min_price')
        max_price = request_get.get('max_price')
        min_term = request_get.get('min_term')
        max_term = request_get.get('max_term')
        min_rate = request_get.get('min_rate')
        max_rate = request_get.get('max_rate')

        search = ProductOptionDocument.search()
        if category_filter:
            i = 0
            q = Q(
                'multi_match',
                query=category_filter[i],
                fields=[
                    'product.category.name'
                ]
            )
            while i < len(category_filter):
                q |= Q(
                    'multi_match',
                    query=category_filter[i],
                    fields=[
                        'product.category.name'
                    ]
                )
                i += 1
            search = search.query(q)
        if min_price:
            search = search.filter('range', price={'gte': min_price})
        if max_price:
            search = search.filter('range', price={'lte': max_price})
        if min_term:
            search = search.filter('range', term={'gte': min_term})
        if max_term:
            search = search.filter('range', term={'lte': max_term})
        if min_rate:
            search = search.filter('range', rate={'gte': min_rate})
        if max_rate:
            search = search.filter('range', rate={'lte': max_rate})

        context['search'] = search
        context['title'] = 'Фильтр'
        context['categories'] = categories
        return context
