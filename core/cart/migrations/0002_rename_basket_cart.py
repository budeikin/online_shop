# Generated by Django 3.2 on 2023-08-17 07:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_module', '0016_comment_comment_like'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Basket',
            new_name='Cart',
        ),
    ]
