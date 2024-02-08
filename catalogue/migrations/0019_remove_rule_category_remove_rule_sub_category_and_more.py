# Generated by Django 5.0.1 on 2024-02-08 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0018_alter_rule_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='category',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='variant',
        ),
        migrations.DeleteModel(
            name='ProductRule',
        ),
        migrations.AddField(
            model_name='rule',
            name='category',
            field=models.ManyToManyField(related_name='rules', to='catalogue.category'),
        ),
        migrations.AddField(
            model_name='rule',
            name='sub_category',
            field=models.ManyToManyField(related_name='rules', to='catalogue.subcategory'),
        ),
        migrations.AddField(
            model_name='rule',
            name='variant',
            field=models.ManyToManyField(related_name='rules', to='catalogue.variant'),
        ),
    ]