# Generated by Django 2.2.4 on 2019-11-12 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_auto_20191110_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='note',
        ),
        migrations.RemoveField(
            model_name='foodbank',
            name='note',
        ),
        migrations.RemoveField(
            model_name='household',
            name='note',
        ),
        migrations.RemoveField(
            model_name='item',
            name='note',
        ),
        migrations.RemoveField(
            model_name='location',
            name='note',
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='donation_time',
            field=models.DateField(blank=True, null=True, verbose_name='捐贈日期'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='有效日期'),
        ),
        migrations.AlterField(
            model_name='sendrecord',
            name='record_time',
            field=models.DateField(blank=True, null=True, verbose_name='領取日期'),
        ),
    ]
