# Generated by Django 5.0.2 on 2024-02-14 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_product_tags_tags_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='tags',
        ),
    ]
