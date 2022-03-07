from django.core.paginator import Paginator, Page
from django.views.generic import ListView
from elasticsearch import RequestError
from elasticsearch_dsl import Q

from main_app.models import ProductCategory, ProductResponse
from search_app.documents import ProductOptionDocument
from search_app.search import search_obj, elastic_filter


class DSEPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        super(DSEPaginator, self).__init__(*args, **kwargs)
        self._count = self.object_list.hits.total

    def page(self, number):
        number = self.validate_number(number)
        return Page(self.object_list, number, self)


class SearchView(ListView):
    """Elastic поиск"""
    template_name = 'search_app/search.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск по запросу:'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        try:
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
            object_list = search_obj(q)

            if object_list.count() == 0:
                try:
                    query = int(query)
                    q = Q(
                        'multi_match',
                        query=query,
                        fields=[
                            'price', 'rate', 'term'
                        ]
                    )
                    object_list = search_obj(q)
                except ValueError:
                    pass
        except RequestError:
            object_list = []
        object_list = elastic_filter(object_list)
        return object_list


class FilterView(ListView):
    """Elastic filter"""
    template_name = 'search_app/search.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.get_categories()
        context['title'] = 'Фильтр'
        context['categories'] = categories
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    def get_queryset(self):
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

        object_list = ProductOptionDocument.search()

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
            object_list = object_list.query(q)
        if min_price:
            object_list = object_list.filter('range', price={'gte': min_price})
        if max_price:
            object_list = object_list.filter('range', price={'lte': max_price})
        if min_term:
            object_list = object_list.filter('range', term={'gte': min_term})
        if max_term:
            object_list = object_list.filter('range', term={'lte': max_term})
        if min_rate:
            object_list = object_list.filter('range', rate={'gte': min_rate})
        if max_rate:
            object_list = object_list.filter('range', rate={'lte': max_rate})

        object_list = elastic_filter(object_list)
        return object_list
