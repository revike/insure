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

        q = Q(
            'multi_match',
            query='english',
            fields=[
                'product.name', 'product.category.name',
                'product.company.name', 'product.short_desc',
                'product.description',
            ],
            fuzziness='auto',
        )

        search = ProductOptionDocument.search().query(q)

        context['search'] = search

        return context
