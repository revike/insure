from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from auth_app.models import CompanyUserProfile, CompanyUser
from cabinet_app.forms import ProfileCreateForm, ProfileUpdateForm, \
    ProfileUpdateDataForm, ProductOptionUpdateForm, ProductUpdateForm, \
    ProductCreateForm, ProductOptionCreateForm
from main_app.models import ProductCategory, ProductOption, PageHit, Product, \
    ProductResponse


class CabinetIndexView(CreateView):
    """Контроллер главной страница личного кабинета"""
    template_name = 'cabinet_app/profile.html'
    form_class = ProfileCreateForm

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        company_id = self.request.user.id
        company = CompanyUserProfile.objects.filter(
            company__id=company_id, company__is_active=True)
        context['title'] = 'личный кабинет'
        context['categories'] = ProductCategory.get_categories()
        context['company'] = company.filter(is_active=True).select_related()
        context['company_not_active'] = company.filter(
            is_active=False).select_related()
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


class ProfileUpdateView(UpdateView):
    """Контроллер редактирования профиля компании"""
    success_url = reverse_lazy('cab_app:profile')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование профиля'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_template_names(self):
        if self.request.resolver_match.url_name == 'profile_update':
            template_name = 'cabinet_app/profile_update.html'
        else:
            template_name = 'cabinet_app/profile_update_data.html'
        return template_name

    def get_form_class(self):
        if self.request.resolver_match.url_name == 'profile_update':
            form_class = ProfileUpdateForm
        else:
            form_class = ProfileUpdateDataForm
        return form_class

    def get_queryset(self):
        if self.request.resolver_match.url_name == 'profile_update':
            queryset = CompanyUserProfile.objects.filter(
                is_active=True, company__is_active=True,
                company_id=self.request.user.id)
        else:
            queryset = CompanyUser.objects.filter(
                is_active=True, id=self.request.user.id)
        return queryset

    def form_valid(self, form):
        if self.request.resolver_match.url_name == 'profile_update_data' \
                and not self.request.user.is_staff:
            CompanyUserProfile.objects.filter(
                company_id=self.request.user.id).update(is_active=False)
            form.save()
            return HttpResponseRedirect(reverse('cab_app:profile'))
        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MyProductListView(ListView):
    """Контроллер списка продуктов компании"""
    model = ProductOption
    template_name = 'cabinet_app/my_products.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'мои продукты'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_queryset(self):
        return ProductOption.objects.filter(
            is_active=True, product__is_active=True,
            product__category__is_active=True,
            product__company__is_active=True,
            product__company__company__is_active=True,
            product__company__company_id=self.request.user.id
        ).select_related()

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MyProductUpdateView(UpdateView):
    """Контроллер редактирования продукта"""
    success_url = reverse_lazy('cab_app:my_products')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование продукта'
        context['categories'] = ProductCategory.get_categories()
        try:
            context['page_hit'] = PageHit.objects.filter(
                url=f'/product/{self.object.id}/').first().count
        except AttributeError:
            context['page_hit'] = 0
        return context

    def get_template_names(self):
        if self.request.resolver_match.url_name == 'product_update':
            template_name = 'cabinet_app/product_update.html'
        else:
            template_name = 'cabinet_app/product_update_title.html'
        return template_name

    def get_form_class(self):
        if self.request.resolver_match.url_name == 'product_update':
            form_class = ProductOptionUpdateForm
        else:
            form_class = ProductUpdateForm
        return form_class

    def form_valid(self, form):
        if self.request.resolver_match.url_name == 'product_update':
            if not form.instance.rate:
                form.instance.rate = 0
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.resolver_match.url_name == 'product_update':
            queryset = ProductOption.objects.filter(
                is_active=True, product__is_active=True,
                product__category__is_active=True,
                product__company__is_active=True,
                product__company__company__is_active=True,
                product__company__company_id=self.request.user.id
            )
        else:
            queryset = Product.objects.filter(
                is_active=True, category__is_active=True,
                company__is_active=True, company__company__is_active=True,
                company__company_id=self.request.user.id)
        return queryset

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MyProductDeleteView(DeleteView):
    """Контроллер удаления продукта"""
    success_url = reverse_lazy('cab_app:my_products')

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'удаление продукта'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_template_names(self):
        if self.request.resolver_match.url_name == 'product_option_delete':
            template_name = 'cabinet_app/product_option_delete.html'
        else:
            template_name = 'cabinet_app/product_delete.html'
        return template_name

    def get_queryset(self):
        if self.request.resolver_match.url_name == 'product_option_delete':
            queryset = ProductOption.objects.filter(
                is_active=True, product__is_active=True,
                product__category__is_active=True,
                product__company__is_active=True,
                product__company__company__is_active=True,
                product__company__company_id=self.request.user.id
            )
        else:
            queryset = Product.objects.filter(
                is_active=True, category__is_active=True,
                company__is_active=True, company__company__is_active=True,
                company__company_id=self.request.user.id)
        return queryset

    def form_valid(self, form):
        product = self.get_object()
        product.is_active = False
        product.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    """Контроллер создания продукта"""
    template_name = 'cabinet_app/product_create.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('cab_app:my_products')
    model = Product

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'создание продукта'
        context['categories'] = ProductCategory.get_categories()
        context['form_product'] = ProductOptionCreateForm
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        form_product = ProductOptionCreateForm(data=request.POST)
        if form.is_valid() and form_product.is_valid():
            company = CompanyUserProfile.objects.filter(
                company_id=self.request.user.id).first()
            form.instance.company_id = company.id
            form.save()
            form_product.instance.product = form.instance
            if not form_product.instance.rate:
                form_product.instance.rate = 0
            form_product.save()
        return HttpResponseRedirect(reverse('cab_app:my_products'))

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductResponseView(ListView):
    """Контроллер отклика на продукт"""
    model = ProductResponse
    template_name = 'cabinet_app/response.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'отклики на продукты'
        context['categories'] = ProductCategory.get_categories()
        return context

    def get_queryset(self):
        user_id = self.request.user.id
        return self.model.objects.filter(
            product__product__company__company__id=user_id).select_related()

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
