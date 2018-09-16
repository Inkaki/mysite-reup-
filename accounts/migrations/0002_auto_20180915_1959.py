# Generated by Django 2.1.1 on 2018-09-15 10:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=200, verbose_name='Accout name')),
            ],
        ),
        migrations.CreateModel(
            name='modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usedDate', models.DateTimeField(default=datetime.datetime(2018, 9, 15, 19, 59, 56, 366608), verbose_name='usedDate')),
                ('item', models.CharField(max_length=20, verbose_name='Item')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('memo', models.CharField(blank=True, max_length=500, verbose_name='memo')),
                ('plan', models.BooleanField(verbose_name='plan')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.account', verbose_name='Account name')),
            ],
            options={
                'verbose_name': 'module',
                'verbose_name_plural': 'module',
                'ordering': ['usedDate'],
                'get_latest_by': 'usedDate',
            },
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='CategoryGroup',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
    ]