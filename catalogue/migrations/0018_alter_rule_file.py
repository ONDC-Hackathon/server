# Generated by Django 5.0.1 on 2024-02-08 08:23

import catalogue.models.rules
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0017_remove_rule_attribute_rule_file_alter_rule_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='file',
            field=models.FileField(blank=True, null=True, storage=catalogue.models.rules.RuleFileStorage(), upload_to=''),
        ),
    ]
