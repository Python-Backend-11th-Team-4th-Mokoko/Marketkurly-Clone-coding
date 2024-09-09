# Generated by Django 5.1 on 2024-09-08 20:06

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('vegetable', '채소'), ('fruits-nuts-rice', '과일·견과·쌀'), ('meat-eggs', '정육·가공육·계란'), ('water-beverages', '생수·음료'), ('furniture-interior', '가구·인테리어'), ('pet', '반려동물')], max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='shop_catego_name_289c7e_idx')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('stock', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=0, max_digits=9)),
                ('available', models.BooleanField(default=True)),
                ('delivery', models.CharField(choices=[('샛별배송', '샛별배송'), ('하루배송', '하루배송'), ('판매자배송', '판매자배송')], max_length=10)),
                ('packaging', models.CharField(choices=[('상온', '상온'), ('냉장', '냉장'), ('냉동', '냉동')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category')),
            ],
            options={
                'ordering': ['product_name'],
                'indexes': [models.Index(fields=['id', 'slug'], name='shop_produc_id_f21274_idx'), models.Index(fields=['product_name'], name='shop_produc_product_8ef27c_idx'), models.Index(fields=['-created'], name='shop_produc_created_ef211c_idx')],
            },
        ),
    ]
