# Generated by Django 2.2.4 on 2019-11-21 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20191117_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='authentication_key',
        ),
    ]
