import uuid
from django.db import models

from apps.base.models import User
from apps.product.models import Product


class Order(models.Model):
    STATUS = (
        (0, 'NEW'),
        (1, 'PROCESS'),
        (2, 'CANCELED'),
        (3, 'FINISHED'),
    )

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    phone = models.CharField(max_length=21)
    address = models.CharField(max_length=221)
    zipcode = models.IntegerField()
    note = models.CharField(max_length=250, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_quantity(self):
        self.quantity = sum([item.quantity for item in self.order_products.all()])
        self.save()
        return self.quantity

    @property
    def get_summa(self):
        self.summa = sum([product.summa for product in self.order_products.all()])
        self.save()
        return self.summa

    def __str__(self):
        return f'order of {self.client}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='products')
    quantity = models.PositiveIntegerField()
    summa = models.FloatField(null=True)

    class Meta:
        unique_together = ['order', 'product']
        ordering = ['product']

        verbose_name = "Buyurtma birlik"
        verbose_name_plural = "Buyurtma birliklar"

    def save(self, *args, **kwargs):
        self.summa = self.product.get_discounted_price() * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product: {self.product}"
