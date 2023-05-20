from modeltranslation.translator import translator, TranslationOptions
from apps.product.models import Product, Category


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'consists')


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
