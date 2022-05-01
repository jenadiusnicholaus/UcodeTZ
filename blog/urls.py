from django.urls import path
from . import views

urlpatterns = [
    path('blog_post/', views.post_view, name ='blog'),
]
