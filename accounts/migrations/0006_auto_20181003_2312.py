# Generated by Django 2.1.1 on 2018-10-03 14:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20181003_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='usedDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 3, 23, 12, 15, 841994), verbose_name='usedDate'),
        ),
    ]