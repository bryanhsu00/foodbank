# Generated by Django 2.2.4 on 2019-10-26 12:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20191018_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='note',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, verbose_name='分類'),
        ),
        migrations.AlterField(
            model_name='category',
            name='note',
            field=models.TextField(blank=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='contacter',
            name='name',
            field=models.CharField(max_length=30, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='expirationrecord',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Item', verbose_name='物品名稱'),
        ),
        migrations.AlterField(
            model_name='expirationrecord',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Location', verbose_name='據點'),
        ),
        migrations.AlterField(
            model_name='expirationrecord',
            name='note',
            field=models.TextField(blank=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='expirationrecord',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='數量'),
        ),
        migrations.AlterField(
            model_name='expirationrecord',
            name='record_time',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='有效期限'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Category', verbose_name='物品分類'),
        ),
        migrations.AlterField(
            model_name='item',
            name='measure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Measure', verbose_name='單位'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=30, verbose_name='物品名稱'),
        ),
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='照片'),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(blank=True, max_length=50, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='location',
            name='foodbank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.FoodBank', verbose_name='食物銀行'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=30, verbose_name='名稱'),
        ),
        migrations.AlterField(
            model_name='location',
            name='note',
            field=models.TextField(blank=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='name',
            field=models.CharField(max_length=30, verbose_name='單位'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='contacter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Contacter', verbose_name='單位聯絡人'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='donation_time',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='捐贈日期'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='donator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Donator', verbose_name='捐贈者'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Item', verbose_name='物品名稱'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Location', verbose_name='捐贈據點'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='note',
            field=models.TextField(blank=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='receiverecord',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='數量'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='expiration_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='有效日期'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Item', verbose_name='物品名稱'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Location', verbose_name='據點'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='數量'),
        ),
        migrations.AlterField(
            model_name='sendrecord',
            name='household',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Household', verbose_name='關懷戶'),
        ),
        migrations.AlterField(
            model_name='sendrecord',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Item', verbose_name='物品名稱'),
        ),
        migrations.AlterField(
            model_name='sendrecord',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Location', verbose_name='領取據點'),
        ),
        migrations.AlterField(
            model_name='sendrecord',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='數量'),
        ),
        migrations.AlterField(
            model_name='sendrecord',
            name='record_time',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='領取日期'),
        ),
    ]