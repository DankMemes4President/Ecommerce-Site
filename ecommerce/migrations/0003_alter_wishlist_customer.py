# Generated by Django 4.0.1 on 2022-01-27 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce', '0002_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.customer'),
        ),
    ]