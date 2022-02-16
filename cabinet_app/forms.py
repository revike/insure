from django import forms
from auth_app.models import CompanyUserProfile, CompanyUser


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
