# Generated by Django 2.2.4 on 2019-10-31 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20191027_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiverecord',
            name='note',
        ),
    ]