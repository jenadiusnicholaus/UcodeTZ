# Generated by Django 3.1.2 on 2020-12-23 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20201223_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='region',
            field=models.CharField(choices=[('Dar', 'Dar es salaam'), ('Ar', 'Arusha'), ('Mw', 'Mwanza'), ('Mb', 'Mbeya')], max_length=10, null=True),
        ),
    ]
