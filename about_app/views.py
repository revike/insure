from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

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
        context['title'] = 'обратная связь'
        context['categories'] = ProductCategory.get_categories()
        context['response_length'] = ProductResponse.get_response_length(
            self.request.user.id)
        return context

    @classmethod
    def post(cls, request, *args, **kwargs):
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user_email = request.POST.get('email')
        user_name = request.POST.get('name')
        send_email_feedback.delay(subject=subject, message=message,
                                  email=user_email, name=user_name)
        send_email_feedback_user.delay(subject=subject, email=user_email,
                                       name=user_name)
        next_url = request.session['next_url']
        if next_url:
            return HttpResponseRedirect(request.session['next_url'])
        return HttpResponseRedirect(reverse('main_app:index'))

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
