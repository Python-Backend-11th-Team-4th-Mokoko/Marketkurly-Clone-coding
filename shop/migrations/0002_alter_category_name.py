# Generated by Django 5.1 on 2024-08-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('vegetable', '채소'), ('fruits-nuts-rice', '과일·견과·쌀'), ('meat-eggs', '정육·가공육·계란'), ('water-beverages', '생수·음료'), ('furniture-interior', '가구·인테리어'), ('pet', '반려동물')], max_length=200),
        ),
    ]
