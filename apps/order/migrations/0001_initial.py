# Generated by Django 4.2.1 on 2023-05-20 07:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('phone', models.CharField(max_length=21)),
                ('address', models.CharField(max_length=221)),
                ('zipcode', models.IntegerField()),
                ('note', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.IntegerField(choices=[(0, 'NEW'), (1, 'PROCESS'), (2, 'CANCELED'), (3, 'FINISHED')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
            options={
                'verbose_name': 'Buyurtma',
                'verbose_name_plural': 'Buyurtmalar',
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('summa', models.FloatField(null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.product')),
            ],
            options={
                'verbose_name': 'Buyurtma birlik',
                'verbose_name_plural': 'Buyurtma birliklar',
                'ordering': ['product'],
                'unique_together': {('order', 'product')},
            },
        ),
    ]
