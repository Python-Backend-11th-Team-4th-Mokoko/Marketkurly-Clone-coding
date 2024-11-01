# Generated by Django 5.1 on 2024-10-22 03:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('order_cost', models.DecimalField(decimal_places=0, max_digits=11)),
                ('deliver_address', models.TextField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-order_date'],
            },
        ),
        migrations.CreateModel(
            name='Ordereditem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_price', models.DecimalField(decimal_places=0, max_digits=9)),
                ('order_quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]
