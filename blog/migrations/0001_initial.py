# Generated by Django 3.1.2 on 2020-12-23 08:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=300, null=True)),
                ('title', models.CharField(max_length=300, null=True)),
                ('description', models.TextField(null=True)),
                ('publish', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
