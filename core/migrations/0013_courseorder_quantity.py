# Generated by Django 3.1.2 on 2020-12-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20201213_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorder',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
