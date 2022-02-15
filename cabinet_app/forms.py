from django import forms

from auth_app.models import CompanyUserProfile


class CompanyProfileCreateForm(forms.ModelForm):
    """Форма создания профиля компании"""

    class Meta:
        model = CompanyUserProfile
        fields = ('name', 'tax_id', 'about_company', 'label')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
