# Generated by Django 3.2 on 2023-08-28 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0021_chart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='change',
            field=models.BooleanField(default=True),
        ),
    ]
