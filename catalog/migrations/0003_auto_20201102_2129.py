# Generated by Django 3.1.3 on 2020-11-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='price',
            field=models.FloatField(),
        ),
    ]