# Generated by Django 3.1.2 on 2020-12-13 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201213_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorder',
            name='courses',
            field=models.ManyToManyField(to='core.EnrolledCourse'),
        ),
    ]
