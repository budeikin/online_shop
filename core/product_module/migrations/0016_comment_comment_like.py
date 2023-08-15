# Generated by Django 3.2 on 2023-08-15 08:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_module', '0015_alter_comment_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_like',
            field=models.ManyToManyField(blank=True, null=True, related_name='com_like', to=settings.AUTH_USER_MODEL),
        ),
    ]