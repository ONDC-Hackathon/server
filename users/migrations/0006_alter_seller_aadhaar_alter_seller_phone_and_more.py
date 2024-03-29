# Generated by Django 5.0.1 on 2024-02-03 04:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_seller_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='aadhaar',
            field=models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_aadhaar_number', message='Enter a valid aadhaar number.', regex='^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$')]),
        ),
        migrations.AlterField(
            model_name='seller',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Enter a valid phone number.', regex='^\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='seller',
            name='pincode',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(code='invalid_pincode', message='Enter a valid pincode.', regex='^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$')]),
        ),
    ]
