# Generated by Django 3.2 on 2023-08-12 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0006_auto_20230811_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='sub_category',
            new_name='parent',
        ),
        migrations.RemoveField(
            model_name='category',
            name='sub_cat',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='product_module.Category'),
        ),
    ]