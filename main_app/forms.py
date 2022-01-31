from django import forms
from main_app.models import ProductResponse


class ProductResponseCreateForm(forms.ModelForm):
    """Форма отклика на продукт"""

    class Meta:
        model = ProductResponse
        fields = (
            'first_name', 'last_name', 'patronymic', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
        self.fields['patronymic'].required = False
        self.fields['first_name'].widget.attrs['placeholder'] = 'Иван'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Иванов'
        self.fields['patronymic'].widget.attrs['placeholder'] = 'Иванович'
        self.fields['email'].widget.attrs['placeholder'] = 'email@email.ru'
        self.fields['phone_number'].widget.attrs[
            'placeholder'] = '+79999999999'
        self.fields['phone_number'].widget.attrs[
            'pattern'] = r'^\+7\d{10,10}$'
