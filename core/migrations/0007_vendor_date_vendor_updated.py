# Generated by Django 5.0.2 on 2024-02-10 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 10, 10, 11, 2, 335917, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
