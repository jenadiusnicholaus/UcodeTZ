# Generated by Django 3.1.2 on 2020-11-19 15:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(null=True, upload_to='course-image')),
                ('courseTitle', models.CharField(max_length=200, null=True)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='BlogContent')),
                ('short_desc', models.TextField(null=True)),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('course_level', models.CharField(choices=[('F', 'Free'), ('P', 'pro')], max_length=200, null=True)),
                ('status', models.CharField(choices=[('0', 'save to Draft'), ('1', 'Publish')], max_length=200, null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.topics')),
            ],
        ),
    ]