# Generated by Django 3.1.2 on 2020-11-20 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201120_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.category'),
        ),
    ]