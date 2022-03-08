from django.contrib import admin

from auth_app.models import CompanyUser, CompanyUserProfile
from auth_app.tasks import send_email_user


class CompanyInline(admin.StackedInline):
    model = CompanyUserProfile


class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyInline,)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        email_user = request.POST.get('email')
        send_email_user.delay(email_user)
        return super().change_view(request, object_id, form_url='',
                                   extra_context=None)


admin.site.register(CompanyUser, CompanyAdmin)
