# Generated by Django 2.1.1 on 2018-10-05 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20181005_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='usedDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 5, 19, 49, 58, 842317), verbose_name='usedDate'),
        ),
    ]
