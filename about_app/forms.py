from captcha.fields import CaptchaField
from django import forms


class FeedBackForm(forms.Form):
    user_name = forms.CharField(label='Имя', required=True)
    user_email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Тема', required=True)
    message = forms.CharField(label='Сообщение', required=True,
                              widget=forms.Textarea)
    Captcha = CaptchaField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

            self.fields['user_name'].widget.attrs[
                'placeholder'] = 'Иванов Иван иванович'
            self.fields['user_email'].widget.attrs[
                'placeholder'] = 'email@email.ru'
            self.fields['subject'].widget.attrs['placeholder'] = 'Тема'
            self.fields['message'].widget.attrs[
                'placeholder'] = 'Текст сообщения'
            self.fields['message'].widget.attrs['cols'] = 24
            self.fields['message'].widget.attrs['rows'] = 5
