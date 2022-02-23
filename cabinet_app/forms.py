from django import forms
from auth_app.models import CompanyUserProfile, CompanyUser
from main_app.models import Product, ProductOption


class ProfileCreateForm(forms.ModelForm):
    """Форма создания профиля компании"""

    class Meta:
        model = CompanyUserProfile
        fields = ('name', 'tax_id', 'about_company', 'label')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProfileUpdateForm(forms.ModelForm):
    """Форма изменения о компании"""

    class Meta:
        model = CompanyUserProfile
        fields = ('about_company', 'label')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProfileUpdateDataForm(forms.ModelForm):
    """Форма изменения профиля компании"""

    class Meta:
        model = CompanyUser
        fields = ('last_name', 'first_name', 'patronymic', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductOptionUpdateForm(forms.ModelForm):
    """Форма редактирования опций продукта"""

    class Meta:
        model = ProductOption
        fields = ('price', 'term', 'rate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductUpdateForm(forms.ModelForm):
    """Форма редактирования продукта"""

    class Meta:
        model = Product
        fields = ('category', 'name', 'short_desc', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
