from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from about_app.forms import FeedBackForm
from about_app.tasks import send_email_feedback, send_email_feedback_user
from main_app.models import ProductCategory, ProductResponse


class ContactView(TemplateView):
    """Контроллер страницы контактов"""
    template_name = 'about_app/contacts.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'контакты'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context


class FeedbackView(TemplateView):
    """Контроллер обратной связи"""
    template_name = 'about_app/feedback.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = 'обратная связь'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        try:
            subject = self.request.session['subject']
        except KeyError:
            subject = ''
        try:
            message = self.request.session['message']
        except KeyError:
            message = ''
        try:
            user_email = self.request.session['user_email']
        except KeyError:
            user_email = ''
        try:
            user_name = self.request.session['user_name']
        except KeyError:
            user_name = ''

        form = FeedBackForm(data={
            'subject': subject,
            'message': message,
            'user_email': user_email,
            'user_name': user_name,
        })
        if user.is_authenticated:
            form = FeedBackForm(data={
                'user_name': f'{user.last_name} '
                             f'{user.first_name} {user.patronymic}',
                'user_email': user.email})
            form.fields['user_name'].widget.attrs[
                'readonly'] = True
            form.fields['user_email'].widget.attrs[
                'readonly'] = True
        context['form'] = form
        self.request.session['subject'] = ''
        self.request.session['message'] = ''
        self.request.session['user_email'] = ''
        self.request.session['user_name'] = ''
        return context

    @classmethod
    def post(cls, request, *args, **kwargs):
        form = FeedBackForm(data=request.POST)
        subject = form.data.get('subject')
        message = form.data.get('message')
        user_email = form.data.get('user_email')
        user_name = form.data.get('user_name')
        if form.is_valid():
            send_email_feedback.delay(subject=subject, message=message,
                                      email=user_email, name=user_name)
            send_email_feedback_user.delay(subject=subject, email=user_email,
                                           name=user_name)
            try:
                next_url = request.session['next_url']
            except KeyError:
                next_url = False
            if next_url:
                return HttpResponseRedirect(request.session['next_url'])
            return HttpResponseRedirect(reverse('main_app:index'))
        request.session['subject'] = subject
        request.session['message'] = message
        request.session['user_email'] = user_email
        request.session['user_name'] = user_name
        return HttpResponseRedirect(reverse('about_app:feedback'))

    def get(self, request, *args, **kwargs):
        next_url = request.META.get('HTTP_REFERER')
        request.session['next_url'] = next_url
        return super().get(request, **kwargs)


class InformationView(TemplateView):
    """Контроллер правовой информации"""
    template_name = 'about_app/information.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'правовая информация'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context


class PoliticsView(TemplateView):
    """Контроллер политики конфиденциальности"""
    template_name = 'about_app/politics.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'политика конфиденциальности'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context


class CookieView(TemplateView):
    """Контроллер Cookies"""
    template_name = 'about_app/cookies.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'cookies'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context
