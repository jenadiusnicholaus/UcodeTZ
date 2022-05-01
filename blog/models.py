from django.db import models


# Create your models here.
from django.utils import timezone


class Post(models.Model):
    image = models.ImageField(upload_to='post_images', null=True)
    slug = models.SlugField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    publish = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

