# Generated by Django 2.2.4 on 2019-11-07 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191018_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='food_bank',
            new_name='foodbank',
        ),
    ]
