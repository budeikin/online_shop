# Generated by Django 3.2 on 2023-08-12 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0008_category_is_sub'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('None', 'none'), ('Size', 'size'), ('Color', 'color')], max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.PositiveIntegerField()),
                ('unit_price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('color_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.productcolor')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='product_module.product')),
                ('size_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.productsize')),
            ],
        ),
    ]