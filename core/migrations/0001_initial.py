# Generated by Django 3.1.2 on 2020-11-06 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('content', models.TextField(null=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('published', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Topics',
            },
        ),
    ]