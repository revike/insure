from django.contrib import admin

from main_app.models import ProductCategory, Product, ProductOption


class InlineProduct(admin.StackedInline):
    model = Product


class CategoryAdmin(admin.ModelAdmin):
    inlines = [InlineProduct]


class InlineOption(admin.TabularInline):
    model = ProductOption


class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineOption]


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
