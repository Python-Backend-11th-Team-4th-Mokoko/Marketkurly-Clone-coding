# Generated by Django 5.1 on 2024-09-03 07:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='delivery',
            field=models.CharField(choices=[('샛별배송', '샛별배송'), ('하루배송', '하루배송'), ('판매자배송', '판매자배송')], max_length=10),
        ),
    ]