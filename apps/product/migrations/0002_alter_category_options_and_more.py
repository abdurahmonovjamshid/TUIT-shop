# Generated by Django 4.2.1 on 2023-05-30 10:29

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent_category',
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='category'),
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True, 'parent__isnull': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='product.category', verbose_name='Parent Category'),
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveIntegerField(default=80),
        ),
        migrations.AlterField(
            model_name='category',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=223, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='consists',
            field=ckeditor.fields.RichTextField(verbose_name="Maxsulot haqida ma'lumot"),
        ),
        migrations.AlterField(
            model_name='product',
            name='consists_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name="Maxsulot haqida ma'lumot"),
        ),
        migrations.AlterField(
            model_name='product',
            name='consists_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name="Maxsulot haqida ma'lumot"),
        ),
        migrations.AlterField(
            model_name='product',
            name='consists_uz',
            field=ckeditor.fields.RichTextField(null=True, verbose_name="Maxsulot haqida ma'lumot"),
        ),
    ]
