# Generated by Django 3.0.8 on 2020-07-29 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_api', '0008_auto_20200728_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='execution',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Archived'),
        ),
    ]
