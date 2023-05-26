from django.db import models
# from django.urls import reverse

# from apps.account.models import Account
from tuitshop import settings
from ckeditor.fields import RichTextField


class Timestamp(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(models.Model):
    class Meta:
        verbose_name = "Mahsulot Kategoriyasi"
        verbose_name_plural = "Mahsulot Kategoriyalari"

    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Parent Category',
                                        limit_choices_to={'is_active': True, 'parent_category__isnull': True},
                                        related_name='children', null=True, blank=True, )
    title = models.CharField(max_length=223)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Brand(Timestamp):
    class Meta:
        verbose_name = "Brend"
        verbose_name_plural = "Brendlar"

    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='product/brands/')

    def __str__(self):
        return self.name


class Product(Timestamp):
    STATUS = (
        (0, 'NEW'),
        (1, 'SALE'),
        (2, 'POPULAR'),
        (3, 'PREMIUM'),
    )

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    status = models.IntegerField(choices=STATUS, default=0, verbose_name="Holati")
    name = models.CharField(max_length=223, null=True, verbose_name="Maxsulot nomi")
    category = models.ManyToManyField(Category, blank=True,
                                      limit_choices_to={'is_active': True, 'parent_category__isnull': False})
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField(verbose_name="Tan narxi")
    discount = models.FloatField(null=True, blank=True, verbose_name="Chegirma")
    made_in = models.CharField(max_length=50, verbose_name="Ishlab chiqarilgan davlat")  # ishlab chiqarilgan joy
    consists = RichTextField(verbose_name="Maxsulot haqida ma'lumot")
    capacity = models.CharField(max_length=20, verbose_name="Maxsulotning og'irligi", null=True, blank=True)  # sig'imi
    guarantee = models.CharField(max_length=30, verbose_name="Maxsulot kafolati", null=True, blank=True)  # muddat
    is_active = models.BooleanField(default=True)

    def get_discounted_price(self):
        if self.discount:
            return self.price - (self.price * (self.discount / 100))
        return self.price

    def __str__(self):
        return f'{self.name}'


class ProductImage(Timestamp):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_images')
    image = models.ImageField(upload_to='product/product_image/')
    is_active = models.BooleanField(default=True)

    @property
    def get_image_url(self):
        if settings.DEBUG:
            return f"{settings.LOCAL_BASE_URL}{self.image.url}"
        else:
            return f"{settings.PROD_BASE_URL}{self.image.url}"

    def __str__(self):
        return f'image of {self.product}'


class Banner(Timestamp):
    class Meta:
        verbose_name = "Banner rasm"
        verbose_name_plural = "Banner rasmlar"

    image = models.ImageField(upload_to='product/banner/')

    def __str__(self):
        return self.image.url
