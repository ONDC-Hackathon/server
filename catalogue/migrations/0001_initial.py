# Generated by Django 5.0.1 on 2024-02-03 04:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_buyer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='catalogue.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='catalogue.subcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], max_length=255)),
                ('avaiable_stock', models.BigIntegerField()),
                ('price', models.DecimalField(decimal_places=5, max_digits=20)),
                ('tax', models.DecimalField(decimal_places=5, max_digits=20)),
                ('discount', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('about', models.JSONField()),
                ('compliance_score', models.DecimalField(decimal_places=5, max_digits=20)),
                ('completeness_score', models.DecimalField(decimal_places=5, max_digits=20)),
                ('correctness_score', models.DecimalField(decimal_places=5, max_digits=20)),
                ('catalogue_score', models.DecimalField(decimal_places=5, max_digits=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='catalogue.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='users.seller')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='catalogue.subcategory')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='catalogue.variant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]