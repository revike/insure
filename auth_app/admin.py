from django.contrib import admin

from auth_app.models import CompanyUser, CompanyUserProfile


class CompanyInline(admin.StackedInline):
    model = CompanyUserProfile


class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyInline,)


admin.site.register(CompanyUser, CompanyAdmin)
