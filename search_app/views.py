from django.views.generic import TemplateView
from elasticsearch_dsl import Q

from main_app.models import ProductCategory
from search_app.documents import ProductOptionDocument


class SearchView(TemplateView):
    """Elastic поиск"""
    template_name = 'search_app/search.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты'
        context['categories'] = ProductCategory.get_categories()

        def search_obj(query_search):
            result = ProductOptionDocument.search().query(query_search)
            res = result.filter('match_phrase', is_active=True).filter(
                'match_phrase', product__is_active=True).filter(
                'match_phrase', product__category__is_active=True).filter(
                'match_phrase', product__company__is_active=True).filter(
                'match_phrase', product__company__company__is_active=True
            ).sort('price', '-rate', '-term')
            return res

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
