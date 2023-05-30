from django.contrib import admin
from .models import Product, ProductImage, Brand, Banner, Category
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin


class CategoryAdmin(DraggableMPTTAdmin, TranslationAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'parent', 'is_active', 'date_created', 'id')
    list_filter = ('parent', 'is_active', 'date_created')
    autocomplete_fields = ('parent',)
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
