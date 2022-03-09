from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from main_app.decorators import counted
from main_app.forms import ProductResponseCreateForm
from main_app.models import ProductCategory, ProductOption, ProductResponse, \
    PageHit
from main_app.tasks import send_email_company
from auth_app.models import CompanyUserProfile


class IndexView(ListView):
    """Контроллер главной страницы"""
    template_name = 'main_app/index.html'
    model = ProductOption

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    def get_queryset(self):
        populate_objects = PageHit.objects.all().order_by('-updated')[:3]
        populate_products = [i.url.split('/')[-2] for i in populate_objects]
        queryset = self.model.objects.filter(
            product_id__in=populate_products, is_active=True,
            product__is_active=True, product__category__is_active=True,
            product__company__is_active=True,
            product__company__company__is_active=True).select_related()
        return queryset


class ProductForCategoryDetailView(ListView):
    """Контроллер списка продуктов для категории"""
    model = ProductCategory
    template_name = 'main_app/category.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        queryset = ProductOption.get_product_for_category(
            category=self.kwargs['pk']).select_related()
        context = super().get_context_data(**kwargs, object_list=queryset)
        categories = ProductCategory.get_categories()
        context['title'] = categories.filter(id=self.kwargs['pk']).first()
        context['categories'] = categories
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    def get_queryset(self):
        """Возвращает список элементов для этого представления"""
        return get_object_or_404(self.model, pk=self.kwargs['pk'])


class ProductListView(ListView):
    """Контроллер списка продуктов"""
    template_name = 'main_app/products.html'
    model = ProductOption
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    def get_queryset(self):
        """Возвращает список элементов для этого представления"""
        object_list = ProductOption.objects.filter(
            is_active=True,
            product__is_active=True,
            product__category__is_active=True,
            product__company__is_active=True,
            product__company__company__is_active=True).select_related()

        # category_filter = []
        # request_get = self.request.GET
        #
        # categories = ProductCategory.get_categories()
        # for category in categories:
        #     if request_get.get(category.name) is not None:
        #         category_filter.append(category)
        #
        # min_price = request_get.get('min_price')
        # max_price = request_get.get('max_price')
        # min_term = request_get.get('min_term')
        # max_term = request_get.get('max_term')
        # min_rate = request_get.get('min_rate')
        # max_rate = request_get.get('max_rate')
        # # search = request_get.get('search')
        #
        # if category_filter:
        #     object_list = object_list.filter(
        #         product__category__in=category_filter)
        # if min_price:
        #     object_list = object_list.filter(price__gte=min_price)
        # if max_price:
        #     object_list = object_list.filter(price__lte=max_price)
        # if min_term:
        #     object_list = object_list.filter(term__gte=min_term)
        # if max_term:
        #     object_list = object_list.filter(term__lte=max_term)
        # if min_rate:
        #     object_list = object_list.filter(rate__gte=min_rate)
        # if max_rate:
        #     object_list = object_list.filter(rate__lte=max_rate)
        # # if search:
        # #     if DATABASES['default']['NAME'] == 'insure':
        # #         vector = SearchVector('product__name',
        # #                               'product__category__name',
        # #                               'product__company__name')
        # #         query = SearchQuery(search)
        # #         object_list = object_list.annotate(
        # #             rank=SearchRank(vector, query)).order_by('-rank')
        # #     else:
        # #         query_string = self.request.GET['search']
        # #         entry_query = get_query(query_string,
        # #                                 ['product__name'])
        # #         object_list = object_list.filter(entry_query)

        return object_list


class ProductDetailView(DetailView):
    """Контроллер продукта"""
    template_name = 'main_app/product.html'
    model = ProductOption

    @counted
    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        form = ProductResponseCreateForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        context['title'] = self.object.product.name
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        """Добавление заявки в базу"""
        form = ProductResponseCreateForm(data=self.request.POST)
        if form.is_valid():
            create_response = form.save(commit=False)
            create_response.product = self.model.objects.get(
                id=self.kwargs['pk'])
            form.save(commit=True)
            instance = form.instance
            send_email_company.delay(
                phone=instance.phone_number, email=instance.email,
                first_name=instance.first_name, last_name=instance.last_name,
                product_name=instance.product.product.name,
                company_email=instance.product.product.company.company.email
            )
            return HttpResponseRedirect(
                reverse('main_app:valid', args=[kwargs['pk']]))
        return HttpResponseRedirect(
            reverse('main_app:product', args=[kwargs['pk']]))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True, product__is_active=True,
                               product__category__is_active=True,
                               product__company__is_active=True,
                               product__company__company__is_active=True)


class ResponseValidView(DetailView):
    """Контроллер удачной заявки"""
    template_name = 'main_app/response_valid.html'
    model = ProductOption

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product.name
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context


class CompanyDetailView(DetailView):
    """Контроллер компании"""
    template_name = 'main_app/company.html'
    model = CompanyUserProfile

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context
