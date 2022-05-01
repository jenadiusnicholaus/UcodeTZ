from django.shortcuts import render
from .models import *


def post_view(request):
    posts = Post.objects.filter(publish=True).order_by('-created_on')
    context = {
        'posts': posts
    }
    return render(request, template_name='blog.html', context=context)
