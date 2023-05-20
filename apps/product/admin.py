from django.contrib import admin
from .models import Product, ProductImage, Brand, Banner, Category
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'parent_category', 'is_active', 'date_created')
    list_filter = ('parent_category', 'is_active', 'date_created')
    autocomplete_fields = ('parent_category',)
    search_fields = ('title',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline]
    list_display = ['id', 'name', 'price', 'discount', 'get_discounted_price', 'status', 'brand', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ('category',)
    list_filter = ('category', 'brand', 'made_in', 'created_at', 'is_active')


admin.site.register(Brand)
admin.site.register(Banner)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
